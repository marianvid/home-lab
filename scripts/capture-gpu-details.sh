#!/usr/bin/env bash
set -euo pipefail

root_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
dist_dir=${HOME_LAB_DIST_DIR:-$root_dir/dist}
capture_dir=${1:-$dist_dir/gpu-detail-capture}
manage_display=${HOME_LAB_MANAGE_DISPLAY:-0}
renderer_pid=

cleanup() {
    [ -z "$renderer_pid" ] || kill "$renderer_pid" 2>/dev/null || true
    rm -f /run/aoostar-next-panel /run/aoostar-details-panel
    if [ "$manage_display" = 1 ]; then
        systemctl start aoostar-display.service
        systemctl start mafp-next-panel.service aoostar-power-button.service
    fi
}
trap cleanup EXIT
if [ "$manage_display" = 1 ]; then
    systemctl stop mafp-next-panel.service aoostar-power-button.service aoostar-display.service
fi
rm -f /run/aoostar-next-panel /run/aoostar-details-panel
mkdir -p "$capture_dir"
cd "$capture_dir"

"$dist_dir/bin/asterctl" --simulate --save \
    --config "$dist_dir/share/home-lab/dashboard.json" \
    --config-dir "$dist_dir/share/home-lab" \
    --font-dir /usr/share/fonts/truetype/dejavu \
    --sensor-path "$root_dir/tests/fixtures/sensors" &
renderer_pid=$!

sleep 5
touch /run/aoostar-next-panel; sleep 5
touch /run/aoostar-next-panel; sleep 5
touch /run/aoostar-details-panel; sleep 5

cleanup
renderer_pid=
trap - EXIT
find "$capture_dir/out" -type f -name 'render_*.png' -print | sort
