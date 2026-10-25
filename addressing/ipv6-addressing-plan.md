# IPv6 addressing plan

The network is **multi-homed**: every segment gets one /52 from each ISP.

- **ISP 1 prefix:** `20AD:1000:1000::/48`
- **ISP 2 prefix:** `30AD:1000:1000::/48`

Subnets use the 4th hextet (the `X000` nibble), which makes the plan easy to read: the same `X000` value means the same segment under both ISPs.

## Level 1: address blocks per ISP

| Block | ISP 1 | ISP 2 |
|---|---|---|
| Infrastructure | `20AD:1000:1000:0000::/52` | `30AD:1000:1000:0000::/52` |
| User | `20AD:1000:1000:2000::/52` | `30AD:1000:1000:2000::/52` |
| Reserved | `20AD:1000:1000:4000::/52` | `30AD:1000:1000:4000::/52` |

## Level 2 and 3: segments and host addresses

| # | ISP 1 subnet | ISP 2 subnet | Purpose | Hosts / interfaces |
|---|---|---|---|---|
| 1 | `20AD:1000:1000:1000::/52` | `30AD:1000:1000:1000::/52` | Birmingham ↔ ISP link | Birmingham Fa0/1 ::2 / ISP 1 Fa0/1 ::1 |
| 2 | `20AD:1000:1000:2000::/52` | `30AD:1000:1000:2000::/52` | Edinburgh ↔ ISP link | Edinburgh Fa1/0 ::2 / ISP 1 Fa1/0 ::1 |
| 3 | `20AD:1000:1000:3000::/52` | `30AD:1000:1000:3000::/52` | Manchester ↔ ISP link | Manchester Fa1/1 ::2 / ISP 1 Fa1/1 ::1 |
| 4 | `20AD:1000:1000:4000::/52` | `30AD:1000:1000:4000::/52` | ISP ↔ London Edge | ISP 1 Fa0/0 ::1 / London Edge Fa0/0 ::2 |
| 5 | `20AD:1000:1000:5000::/52` | `30AD:1000:1000:5000::/52` | London Edge ↔ London DMZ | Edge Fa0/1 ::1 / DMZ Fa0/1 ::2 |
| 6 | `20AD:1000:1000:6000::/52` | `30AD:1000:1000:6000::/52` | London DMZ: email server (VLAN 100) | Gateway ::1 · Email server ::100 |
| 7 | `20AD:1000:1000:7000::/52` | `30AD:1000:1000:7000::/52` | London DMZ: financial floor (VLAN 200) | Gateway ::1 · Financial team server ::200 · Sub-file server ::203 |
| 8 | `20AD:1000:1000:8000::/52` | `30AD:1000:1000:8000::/52` | London Edge ↔ London Internal | Edge Fa1/0 ::1 / Internal Fa1/0 ::2 |
| 9 | `20AD:1000:1000:9000::/52` | `30AD:1000:1000:9000::/52` | Manchester internal LAN | Gateway ::1 · Manchester PC ::100 |
| 10 | `20AD:1000:1000:A000::/52` | `30AD:1000:1000:A000::/52` | Birmingham internal LAN | Gateway ::1 · Birmingham PC ::100 |
| 11 | `20AD:1000:1000:B000::/52` | `30AD:1000:1000:B000::/52` | Edinburgh internal LAN | Gateway ::1 · Edinburgh PC ::100 |
| 12 | `20AD:1000:1000:C000::/52` | `30AD:1000:1000:C000::/52` | London Internal: web server (VLAN 201) | Gateway ::1 · Web server ::201 |
| 13 | `20AD:1000:1000:D000::/52` | `30AD:1000:1000:D000::/52` | London Internal: employees (VLAN 202) | Gateway ::1 · Employee PC1 ::202 · Employee PC2 ::204 |
| 14 | `20AD:1000:1000:E000::/52` | `30AD:1000:1000:E000::/52` | FG3 (reserved in plan) | not assigned in report |
| 15 | `20AD:1000:1000:F000::/52` | `30AD:1000:1000:F000::/52` | Manchester Wi-Fi service | Manchester ::2 · Wi-Fi (config side) ::100 |

## Router IDs (OSPFv3, area 0)

| Router | Router ID |
|---|---|
| Birmingham | 1.1.1.1 |
| Edinburgh | 2.2.2.2 |
| Manchester | 3.3.3.3 |
| ISP 1 | 4.4.4.4 |
| London Edge | 5.5.5.5 |
| London DMZ | 6.6.6.6 |
| London Internal | 7.7.7.7 |
| ISP 2 | 8.8.8.8 |

## Notes

- Source: ICA 1 report, section 11 (pages 16–26). Interface names come from the ICA 2 router configs.
- **Correction:** in the original report, the ISP 2 tables repeat the "ISP 1" labels from the ISP 1 table. The router configs show that every `30AD:` link connects to **ISP 2**, so this table labels them that way.
- Manchester's ISP 2 interface is not shown in the report (its config screenshot is partial), so its interface name is not listed.
- Gateways use `::1` and hosts use `::100` and up, which makes addresses quick to recognise in logs.
