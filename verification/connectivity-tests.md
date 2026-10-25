# Connectivity verification

All tests were run in Cisco Packet Tracer from the **Birmingham PC** (`20AD:1000:1000:A000::100`), with 4 ICMPv6 echo requests each. Starting from one remote site and reaching every other site and server proves that routing, the WAN links and the VLAN sub-interfaces all work end to end.

| # | Destination | Address pinged | Result | Avg RTT | Report page |
|---|---|---|---|---|---|
| 1 | Birmingham router (gateway) | `20AD:1000:1000:A000::1` | ✅ 4/4 replies, 0% loss | 3 ms | 12 |
| 2 | ISP 1 router | `20AD:1000:1000:1000::1` | ✅ 4/4 replies, 0% loss | 8 ms | 13 |
| 3 | ISP 2 router | `30AD:1000:1000:1000::1` | ⚠️ see note | not captured* | 13 |
| 4 | London Edge router | `20AD:1000:1000:4000::2` | ✅ 4/4 replies, 0% loss | 0 ms | 14 |
| 5 | London DMZ router | `20AD:1000:1000:5000::2` | ✅ 4/4 replies, 0% loss | 27 ms | 14 |
| 6 | Email server (DMZ, VLAN 100) | `20AD:1000:1000:6000::100` | ✅ 4/4 replies, 0% loss | 18 ms | 15 |
| 7 | Financial team server (DMZ, VLAN 200) | `20AD:1000:1000:7000::200` | ✅ 4/4 replies, 0% loss | 12 ms | 15 |
| 8 | Sub-file server (DMZ, VLAN 200) | `20AD:1000:1000:7000::203` | ✅ 4/4 replies, 0% loss | 14 ms | 16 |
| 9 | Web server (London Internal, VLAN 201) | `20AD:1000:1000:C000::201` | ✅ 4/4 replies, 0% loss | 15 ms | 16 |
| 10 | Employee PC1 (London Internal, VLAN 202) | `20AD:1000:1000:D000::202` | ✅ 4/4 replies, 0% loss | 29 ms | 17 |
| 11 | Employee PC2 (London Internal, VLAN 202) | `20AD:1000:1000:D000::204` | ✅ 4/4 replies, 0% loss | 22 ms | 17 |
| 12 | Manchester Wi-Fi service (config side) | `20AD:1000:1000:F000::100` | ✅ 4/4 replies, 0% loss | 8 ms | 18 |
| 13 | Edinburgh PC | `20AD:1000:1000:B000::100` | ✅ 4/4 replies, 0% loss | 22 ms | 18 |
| 14 | Manchester PC | `20AD:1000:1000:9000::100` | ✅ 4/4 replies, 0% loss | 54 ms | 19 |

**Result: 13 of 14 tests have a captured screenshot, and all 13 show 0% packet loss.**

\* Test 3 (ISP 2): the report reuses the screenshot from test 2 (a ping to ISP 1), so no separate result was captured for ISP 2. It should be re-tested to document the ISP 2 path properly.

## Notes

- Results were read from the terminal screenshots in the ICA 2 report (section 13.1, pages 12–19).
- Some test headings in the report differ from the address actually pinged (tests 4, 5 and 12). This table lists the address shown in each screenshot.
- Sample screenshot: [`../images/ping-birmingham-to-file-server.jpg`](../images/ping-birmingham-to-file-server.jpg)

## Re-running the tests

From the Birmingham PC in Packet Tracer (Desktop → Command Prompt):

```
ping 20AD:1000:1000:A000::1
ping 30AD:1000:1000:1000::1
ping 20AD:1000:1000:6000::100
ping 20AD:1000:1000:C000::201
ping 20AD:1000:1000:9000::100
```

Useful router checks:

```
show ipv6 ospf neighbor
show ipv6 route ospf
show ipv6 interface brief
```
