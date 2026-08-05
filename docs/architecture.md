# Architecture

Small systemd-supervised components keep collection, rendering and input
separate:

1. `aster-sysinfo` publishes generic system metrics.
2. MARIAN LAB sensors add Proxmox, network, mount and NVMe SMART state.
3. Patched `asterctl` renders the selected panel.
4. A persistent MAFP helper turns touch duration into tap/hold triggers.
5. A power-event helper opens the guarded System Actions modal.

Top-level panels are Health, Compute, Storage, Network and Services. Child
panels use `Parent > Child` names, allowing navigation to discover them without
hard-coded panel counts. Missing removable disks are omitted, not reported as
failed placeholders.

Health states are OK, Warning and Critical. Unavailable data is never silently
presented as a healthy zero. Critical conditions include SMART/media failures,
unsafe temperature and required-service failure.
