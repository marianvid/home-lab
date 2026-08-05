#!/usr/bin/env bash
set -euo pipefail

root_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
dist_dir=${MARIAN_LAB_DIST_DIR:-$root_dir/dist}
capture_dir=${1:-$dist_dir/gallery-capture}
manage_display=${MARIAN_LAB_MANAGE_DISPLAY:-0}
renderer_pid=

cleanup() {
    if [ -n "$renderer_pid" ]; then
        kill "$renderer_pid" 2>/dev/null || true
        wait "$renderer_pid" 2>/dev/null || true
    fi
    rm -f /run/aoostar-next-panel
    if [ "$manage_display" = 1 ]; then
        systemctl start aoostar-display.service
    fi
}
trap cleanup EXIT

if [ "$manage_display" = 1 ]; then
    systemctl stop aoostar-display.service
fi
rm -f /run/aoostar-next-panel /run/aoostar-details-panel
mkdir -p "$capture_dir"
cd "$capture_dir"

"$dist_dir/bin/asterctl" --simulate --save \
    --config "$dist_dir/share/marian-lab/dashboard.json" \
    --config-dir "$dist_dir/share/marian-lab" \
    --font-dir /usr/share/fonts/truetype/dejavu \
    --sensor-path "$root_dir/tests/fixtures/sensors" &
renderer_pid=$!

sleep 5
for _panel in 2 3 4 5; do
    touch /run/aoostar-next-panel
    sleep 5
done

cleanup
renderer_pid=
trap - EXIT

find "$capture_dir/out" -type f -name 'render_*.png' -print | sort
