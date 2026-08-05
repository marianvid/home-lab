#!/usr/bin/env bash
set -euo pipefail

root_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
build_dir=${MARIAN_LAB_BUILD_DIR:-$root_dir/build}
dist_dir=${MARIAN_LAB_DIST_DIR:-$root_dir/dist}
aoostar_commit=2f4d95957d2d61f9fe5cd27e4cf14bd2ae566f63
libfprint_commit=c4654fdc85c25afdd9115bec2f95a44145ae3b94

if [ "${1:-}" = "--clean" ]; then
    rm -rf -- "$build_dir" "$dist_dir"
elif [ $# -gt 0 ]; then
    echo "Usage: $0 [--clean]" >&2
    exit 2
fi

missing=0
for command_name in git cargo rustc meson ninja pkg-config gcc python3; do
    command -v "$command_name" >/dev/null 2>&1 || {
        echo "Missing required command: $command_name" >&2
        missing=1
    }
done
for module in glib-2.0 gio-2.0 gusb; do
    pkg-config --exists "$module" || {
        echo "Missing pkg-config module: $module" >&2
        missing=1
    }
done
[ "$missing" -eq 0 ] || exit 1

mkdir -p "$build_dir" "$dist_dir/bin" "$dist_dir/share/marian-lab/img" \
    "$dist_dir/systemd" "$dist_dir/config" "$dist_dir/rootfs"

checkout_source() {
    local name=$1 repo=$2 commit=$3 destination=$4
    if [ ! -d "$destination/.git" ]; then
        git clone --filter=blob:none "$repo" "$destination"
    fi
    git -C "$destination" fetch --force origin "$commit"
    git -C "$destination" checkout --detach "$commit"
    git -C "$destination" reset --hard "$commit"
    git -C "$destination" clean -fdx
    printf 'Checked out %s at %s\n' "$name" "$commit"
}

aoostar_src=$build_dir/aoostar-rs
checkout_source aoostar-rs https://github.com/zehnm/aoostar-rs.git \
    "$aoostar_commit" "$aoostar_src"
git -C "$aoostar_src" apply --check "$root_dir/patches/aoostar-rs-marian-lab.patch"
git -C "$aoostar_src" apply "$root_dir/patches/aoostar-rs-marian-lab.patch"
cargo build --manifest-path "$aoostar_src/Cargo.toml" --release --locked \
    -p asterctl -p aster-sysinfo
install -m 0755 "$aoostar_src/target/release/asterctl" "$dist_dir/bin/asterctl"
install -m 0755 "$aoostar_src/target/release/aster-sysinfo" "$dist_dir/bin/aster-sysinfo"

libfprint_src=$build_dir/libfprint
checkout_source libfprint https://gitlab.freedesktop.org/libfprint/libfprint.git \
    "$libfprint_commit" "$libfprint_src"
git -C "$libfprint_src" apply --check "$root_dir/patches/libfprint-mafp-touch-mode.patch"
git -C "$libfprint_src" apply "$root_dir/patches/libfprint-mafp-touch-mode.patch"
meson setup "$libfprint_src/build" "$libfprint_src" \
    --prefix=/opt/libfprint-mafp --libdir=lib \
    -Ddrivers=mafpmoc -Dintrospection=false -Ddoc=false \
    -Dinstalled-tests=false -Dgtk-examples=false \
    -Dudev_rules=disabled -Dudev_hwdb=disabled
meson compile -C "$libfprint_src/build"
DESTDIR="$dist_dir/rootfs" meson install -C "$libfprint_src/build"

uninstalled_pc=$libfprint_src/build/meson-uninstalled
pc_path="$uninstalled_pc${PKG_CONFIG_PATH:+:$PKG_CONFIG_PATH}"
for helper in mafp-next-panel mafp-calibrate; do
    PKG_CONFIG_PATH="$pc_path" gcc -O2 -Wall -Wextra \
        "$root_dir/dashboard/runtime/$helper.c" -o "$dist_dir/bin/$helper" \
        $(PKG_CONFIG_PATH="$pc_path" pkg-config --cflags --libs libfprint-2) \
        -Wl,-rpath,/opt/libfprint-mafp/lib
done
gcc -O2 -Wall -Wextra "$root_dir/dashboard/runtime/aoostar-power-button.c" \
    -o "$dist_dir/bin/aoostar-power-button"

install -m 0755 "$root_dir/dashboard/runtime/aoostar-lab-sensors" \
    "$dist_dir/bin/marian-lab-sensors"
install -m 0755 "$root_dir/dashboard/runtime/aoostar-health-monitor" \
    "$dist_dir/bin/marian-lab-health-monitor"
install -m 0644 "$root_dir/dashboard/config/dashboard.json" \
    "$dist_dir/share/marian-lab/dashboard.json"
cp -a "$root_dir/dashboard/assets/." "$dist_dir/share/marian-lab/img/"
cp -a "$root_dir/systemd/." "$dist_dir/systemd/"
cp -a "$root_dir/dashboard/config/." "$dist_dir/config/"

cat > "$dist_dir/BUILD-METADATA.txt" <<EOF
MARIAN LAB build
aoostar-rs=$aoostar_commit
libfprint=$libfprint_commit
rustc=$(rustc --version)
meson=$(meson --version)
built_at=$(date --iso-8601=seconds)
EOF

echo "Build completed without installing or modifying host configuration."
echo "Artifacts: $dist_dir"
