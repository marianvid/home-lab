# Privacy and security

With `MAFP_TOUCH_MODE` enabled, the patched MAFP driver reports finger presence
and release, then returns to waiting before feature extraction, matching or
enrollment. The dashboard creates, stores and transmits no biometric template.

The custom libfprint tree is staged for an isolated `/opt/libfprint-mafp` prefix
instead of silently overwriting the distribution package.

Public files exclude SSH material, host IPs, usernames, disk serial numbers and
private inventories. Stable disk IDs belong in an ignored local configuration.

These safeguards describe intent and tested behavior, not a security guarantee.
Read [DISCLAIMER.md](../DISCLAIMER.md).
