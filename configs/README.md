# Device configurations

Cisco IOS configs for the 8 routers and 3 switches in the network, built in **Cisco Packet Tracer**.

| File | Device | Router ID | Status |
|---|---|---|---|
| `routers/R1-birmingham.cfg` | Birmingham branch router | 1.1.1.1 | Complete excerpt |
| `routers/R2-edinburgh.cfg` | Edinburgh branch router | 2.2.2.2 | Complete excerpt |
| `routers/R3-manchester.cfg` | Manchester branch router | 3.3.3.3 | **Partial** (see below) |
| `routers/R4-isp1.cfg` | ISP 1 | 4.4.4.4 | Complete excerpt |
| `routers/R5-london-edge.cfg` | London Edge (HQ) | 5.5.5.5 | Complete excerpt |
| `routers/R6-london-dmz.cfg` | London DMZ | 6.6.6.6 | **Partial** (see below) |
| `routers/R7-london-internal.cfg` | London Internal | 7.7.7.7 | Complete excerpt |
| `routers/R8-isp2.cfg` | ISP 2 | 8.8.8.8 | Complete excerpt |
| `switches/london-dmz-multilayer.cfg` | DMZ multilayer switch | – | Trunk ports |
| `switches/london-dmz-ac1.cfg` | DMZ access switch AC1 | – | Trunks + VLAN 100 access port |
| `switches/london-dmz-ac2.cfg` | DMZ access switch AC2 | – | Trunk ports |

## Where these came from

These are transcribed from the `show running-config` screenshots in the ICA 2 report (section 13.2, pages 20–24). The screenshots show the interface and OSPFv3 sections of each config.

- Lines starting with `! [added]` or `! [added note]` were **not** in the screenshots. They are comments added for readability (for example, which device a link connects to) or for completeness (`hostname`, `ipv6 unicast-routing`). Because they are comments, IOS ignores them.
- **Manchester (R3):** the screenshot starts at `FastEthernet1/1`, so the LAN, ISP 2 and Wi-Fi interfaces are missing.
- **London DMZ (R6):** the first sub-interface header (email server segment, VLAN 100) is cut off in the screenshot.

## Key design points visible in the configs

- **OSPFv3 everywhere:** every routed interface runs `ipv6 ospf 1 area 0`, with a unique router ID per router (1.1.1.1 to 8.8.8.8).
- **Dual addressing for multi-homing:** core links carry an address from both ISP prefixes (`20AD:` and `30AD:`), so traffic can use either provider.
- **Router-on-a-stick VLANs:** London DMZ and London Internal use 802.1Q sub-interfaces (`Fa0/0.200`, `Fa0/0.201`, `Fa0/0.202`) to route between VLANs.
- **Unused ports shut down:** spare interfaces are administratively `shutdown`, a basic hardening step.

## Check them

```bash
python3 scripts/check_configs.py
```

This checks router IDs are unique, every address is inside an ISP prefix, both ends of each link match, and every subnet is in the addressing plan.
