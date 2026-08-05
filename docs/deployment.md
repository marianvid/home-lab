# Manual deployment reference

This is deliberately **not** an installer. Every command and path must be
reviewed and adapted to the target machine. Keep independent recovery access.

## 1. Inspect the build

Run the clean build and smoke test, then inspect `dist/`, both upstream patches,
all systemd units and the local device configuration example. Do not proceed if
the target hardware IDs or input paths differ from the tested platform.

## 2. Preserve originals

Back up any existing LCD binary, libfprint customization, systemd unit and
logind configuration. Record ownership and modes. A rollback should be possible
without network access.

## 3. Adapt local configuration

Copy `dashboard/config/devices.conf.example` to a root-only local file and set
stable `/dev/disk/by-id` paths, mount point and network interface. Never commit
that file; disk IDs can be unique identifiers.

The power helper currently targets the tested AOOSTAR ACPI input path:
`/dev/input/by-path/platform-PNP0C0C:00-event`. Verify it through `/dev/input`
and kernel events before compiling or deploying the helper on another system.

## 4. Stage, then deploy deliberately

The reference deployment maps build artifacts as follows:

| Build artifact | Reference destination |
| --- | --- |
| `dist/bin/asterctl` | `/usr/local/bin/asterctl` |
| `dist/bin/aster-sysinfo` | `/usr/local/bin/aster-sysinfo` |
| `dist/rootfs/opt/libfprint-mafp` | `/opt/libfprint-mafp` |
| dashboard assets/config | `/opt/aoostar-display` |
| gesture and power helpers | `/opt/aoostar-display` |
| reviewed units | `/etc/systemd/system` |
| local device config | `/etc/home-lab/devices.conf` |

Copying is intentionally left to the administrator. Use a staging directory,
compare files, preserve backups and reload systemd only after verification.

## 5. Power-button safety

The logind override makes a normal Power press do nothing by itself. Activate it
only together with a tested watcher and an alternative administrative shutdown
path. Validate the five-second cancellation before enabling the unit at boot.

## 6. ASPM is optional and host-specific

The reference AOOSTAR is stable with `pcie_aspm=off`. This is not a universal
requirement and can increase idle power. Treat it as a troubleshooting measure,
not a default installation step. Kernel-command-line changes require deliberate
bootloader updates and a recovery plan.

## 7. Hardware acceptance test

Before enabling at boot, confirm:

- simulator output and JSON parsing;
- real LCD rendering and recovery after service restart;
- tap versus hold behavior without biometric enrollment;
- Storage health with present and absent removable devices;
- System Actions toggle, timeout and explicit confirmation;
- remote access, boot and controlled rollback.
