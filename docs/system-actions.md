# Guarded System Actions

A normal short Power press opens a modal LCD menu instead of immediately
stopping the server. A sensor tap toggles Reboot/Shutdown, a hold confirms, and
five seconds without input cancels and restores the previous dashboard panel.

The menu is not part of normal panel navigation and can be opened only through
the physical Power button. systemd-logind ignores the default short-press action;
a dedicated ACPI/input watcher requests the menu. Reboot or shutdown executes
only after explicit hold confirmation.

After confirmation, the selection menu is immediately replaced by a dedicated
`REBOOTING` or `SHUTTING DOWN` panel. A separate orchestrator reports real guest
counts while stopping VMs and containers, synchronizes storage, and only then
requests the final reboot or poweroff. This keeps the LCD informative instead
of leaving the stale selection menu on screen.

During startup, the firmware logo remains visible until Linux can access the
LCD. The startup helper then shows system initialization, network and Proxmox
service readiness before releasing the display back to the normal Health panel.

The firmware-controlled long hardware press remains an emergency hard cutoff.
It is deliberately not a normal menu option because it can cause data loss.

The gallery documents both selected states with sanitized renderer captures.
