# Guarded System Actions

A normal short Power press opens a modal LCD menu instead of immediately
stopping the server. A sensor tap toggles Reboot/Shutdown, a hold confirms, and
five seconds without input cancels and restores the previous dashboard panel.

The menu is not part of normal panel navigation and can be opened only through
the physical Power button. systemd-logind ignores the default short-press action;
a dedicated ACPI/input watcher requests the menu. Reboot or shutdown executes
only after explicit hold confirmation.

The firmware-controlled long hardware press remains an emergency hard cutoff.
It is deliberately not a normal menu option because it can cause data loss.

The gallery documents both selected states with sanitized renderer captures.
