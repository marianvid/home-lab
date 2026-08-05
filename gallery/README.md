#Dashboard Gallery

Renderer-generated captures at the native LCD resolution of **960×376**. All
values are synthetic or anonymized documentation fixtures; no private host IP,
disk serial number or personal workload data is shown.

Click any panel to open the full-resolution image.

## Main dashboard

<table>
  <tr>
    <td width="50%" align="center">
      <a href="health.png"><img src="health.png" width="460" alt="Health panel"></a><br>
      <strong>Health</strong><br>
      Compact state of Compute, Storage, Network and Services.
    </td>
    <td width="50%" align="center">
      <a href="compute.png"><img src="compute.png" width="460" alt="Compute panel"></a><br>
      <strong>Compute</strong><br>
      CPU, GPU, memory, load, clocks and uptime.
    </td>
  </tr>
  <tr>
    <td width="50%" align="center">
      <a href="storage.png"><img src="storage.png" width="460" alt="Adaptive Storage panel"></a><br>
      <strong>Storage</strong><br>
      Adaptive internal/external device layout without empty placeholders.
    </td>
    <td width="50%" align="center">
      <a href="network.png"><img src="network.png" width="460" alt="Network panel"></a><br>
      <strong>Network</strong><br>
      Link, live throughput, interface, gateway and traffic totals.
    </td>
  </tr>
  <tr>
    <td width="50%" align="center">
      <a href="services.png"><img src="services.png" width="460" alt="Services panel"></a><br>
      <strong>Services</strong><br>
      Proxmox, MARIAN LAB, guests, storage, SSH and node state.
    </td>
    <td width="50%"></td>
  </tr>
</table>

<br><br>

## Storage details

<table>
  <tr>
    <td width="50%" align="center">
      <a href="storage-lexar-details.png"><img src="storage-lexar-details.png" width="460" alt="Internal NVMe details"></a><br>
      <strong>Internal NVMe</strong><br>
      SMART, wear, written data, hours, AVL/CAP and media errors.
    </td>
    <td width="50%" align="center">
      <a href="storage-corsair-details.png"><img src="storage-corsair-details.png" width="460" alt="External USB4 NVMe details"></a><br>
      <strong>External USB4/NVMe</strong><br>
      Filesystem availability plus native NVMe health information.
    </td>
  </tr>
</table>

<br><br>

## Health-state language

<table>
  <tr>
    <td width="33%" align="center">
      <a href="health-warning.png"><img src="health-warning.png" width="300" alt="Warning state"></a><br>
      <strong>Warn</strong><br>Fixed amber dot.
    </td>
    <td width="33%" align="center">
      <a href="health-error-on.png"><img src="health-error-on.png" width="300" alt="Error pulse visible"></a><br>
      <strong>Err — pulse on</strong><br>Red dot visible.
    </td>
    <td width="33%" align="center">
      <a href="health-error-off.png"><img src="health-error-off.png" width="300" alt="Error pulse hidden"></a><br>
      <strong>Err — pulse off</strong><br>Text remains readable.
    </td>
  </tr>
</table>

<br><br>

## Guarded System Actions

The physical Power button opens this private modal; it is not part of normal
dashboard rotation. Tap changes the selection, hold confirms, and the menu
cancels after five seconds without input.

<table>
  <tr>
    <td width="50%" align="center">
      <a href="system-actions-reboot.png"><img src="system-actions-reboot.png" width="460" alt="Reboot selected"></a><br>
      <strong>Reboot selected</strong>
    </td>
    <td width="50%" align="center">
      <a href="system-actions-shutdown.png"><img src="system-actions-shutdown.png" width="460" alt="Shutdown selected"></a><br>
      <strong>Shutdown selected</strong>
    </td>
  </tr>
</table>

See the [project README](../README.md) for architecture, build instructions,
safety notices and the Human–AI collaboration disclosure.
