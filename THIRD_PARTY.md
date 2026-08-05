# Third-party notices

## aoostar-rs

- <https://github.com/zehnm/aoostar-rs>
- Original developer: [Markus Zehnder (`@zehnm`)](https://github.com/zehnm)
- Tested commit: `2f4d95957d2d61f9fe5cd27e4cf14bd2ae566f63`
- License: MIT OR Apache-2.0

`aoostar-rs` reverse-engineered the undocumented AOOSTAR display protocol and
provides the Rust LCD control and sensor-panel renderer on which HOME LAB is
built. The HOME LAB patch adds manual hierarchical navigation, responsive
triggers, guarded system actions and adaptive Storage rendering.

## libfprint

- <https://gitlab.freedesktop.org/libfprint/libfprint.git>
- Tested commit: `c4654fdc85c25afdd9115bec2f95a44145ae3b94`
- License: LGPL-2.1-or-later

The patch adds an opt-in MAFP touch-only mode that avoids biometric feature
generation and exposes only contact/release behavior to the local helper.
