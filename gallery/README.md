# Dashboard Gallery

Renderer-generated captures at the native LCD resolution of **960×376**. All
values are synthetic or anonymized documentation fixtures; no private host IP,
disk serial number or personal workload data is shown.

Click any panel to open the full-resolution image.

## Main dashboard

<table>
  <tr>
    <td width="50%" align="center">
      <a href="health.png"><img src="health.png" width="460" alt="Health panel"></a><br>
      <small><em><strong>Health</strong><br>
      Compact state of Compute, Storage, Network and Services.</em></small><br><br>
    </td>
    <td width="50%" align="center">
      <a href="compute.png"><img src="compute.png" width="460" alt="Compute panel"></a><br>
      <small><em><strong>Compute</strong><br>
      CPU, GPU, memory, load, clocks and uptime.</em></small><br><br>
    </td>
  </tr>
  <tr>
    <td width="50%" align="center">
      <a href="gpu.png"><img src="gpu.png" width="460" alt="Dynamic NVIDIA GPU panel"></a><br>
      <small><em><strong>NVIDIA GPU</strong><br>
      Live temperature, load, VRAM, power, fan, workload and health.</em></small><br><br>
    </td>
    <td width="50%" align="center">
      <a href="gpu-details.png"><img src="gpu-details.png" width="460" alt="NVIDIA GPU details"></a><br>
      <small><em><strong>GPU details</strong><br>
      Driver, CUDA, clocks, persistence, ECC, PCI address and Xid errors.</em></small><br><br>
    </td>
  </tr>
  <tr>
    <td width="50%" align="center">
      <a href="storage.png"><img src="storage.png" width="460" alt="Adaptive Storage panel"></a><br>
      <small><em><strong>Storage</strong><br>
      Adaptive internal/external device layout.</em></small><br><br>
    </td>
    <td width="50%" align="center">
      <a href="network.png"><img src="network.png" width="460" alt="Network panel"></a><br>
      <small><em><strong>Network</strong><br>
      Link, live throughput, interface, gateway and traffic totals.</em></small><br><br>
    </td>
  </tr>
  <tr>
    <td width="50%" align="center">
      <a href="services.png"><img src="services.png" width="460" alt="Services panel"></a><br>
      <small><em><strong>Services</strong><br>
      Proxmox, dashboard services, guests, storage, SSH and node state.</em></small>
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
      <small><em><strong>Internal NVMe</strong><br>
      SMART, wear, written data, hours, AVL/CAP and media errors.</em></small>
    </td>
    <td width="50%" align="center">
      <a href="storage-corsair-details.png"><img src="storage-corsair-details.png" width="460" alt="External USB4 NVMe details"></a><br>
      <small><em><strong>External USB4/NVMe</strong><br>
      Filesystem availability plus native NVMe health information.</em></small>
    </td>
  </tr>
</table>

<br><br>

## Health-state language

<table>
  <tr>
    <td width="50%" align="center">
      <a href="health-warning.png"><img src="health-warning.png" width="460" alt="Warning state"></a><br>
      <small><em><strong>Warn</strong><br>Fixed amber dot.</em></small>
    </td>
    <td width="50%" align="center">
      <a href="health-error-on.png"><img src="health-error-on.png" width="460" alt="Error pulse visible"></a><br>
      <small><em><strong>Err — pulse on</strong><br>Red dot visible.</em></small>
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
      <small><em><strong>Reboot selected</strong></em></small>
    </td>
    <td width="50%"></td>
  </tr>
</table>

See the [project README](../README.md) for architecture, build instructions,
safety notices and the Human–AI collaboration disclosure.
