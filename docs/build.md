# Reproducible build

`scripts/build.sh` starts from pinned upstream commits and writes only to
`build/` and `dist/`. It does not install anything or access the hardware.

The complete pipeline is tested on Debian 13 / Proxmox VE 9.2.2. It requires
Git, GCC, Rust/Cargo, Meson, Ninja, pkg-config, GLib/GIO, GUsb and Python 3.

Representative Debian dependencies:

```bash
apt install build-essential git meson ninja-build pkg-config \
  libglib2.0-dev libgusb-dev libudev-dev python3 fonts-dejavu-core
```

Then run:

```bash
./scripts/build.sh --clean
./scripts/test-dist.sh
```

The pipeline checks out exact revisions, verifies patches with `git apply
--check`, compiles aoostar-rs and isolated libfprint, compiles the local helpers,
and packages dashboard/configuration examples. `test-dist.sh` validates expected
artifacts, JSON and shell syntax and renders a panel with anonymous fixture data.

Pinned commits are a safety boundary. Updating them requires refreshing patches
and repeating clean-build, simulation and real-hardware tests.
