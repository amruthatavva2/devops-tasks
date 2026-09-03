# Networking Homework Tasks

## Task 1: Practice material from the shared repository

Repository reviewed: [Nency-Ravaliya/devops-heros](https://github.com/Nency-Ravaliya/devops-heros/)

The repository contains IP-addressing and subnetting notes in `session4-networking`, plus a Linux Networking Cheat Sheet in `session2-linux`. I used those materials to revise the following topics.

### What I understood about IP addressing

- An IP address identifies a device on an IP network. IPv4 addresses contain 32 bits, normally written as four decimal numbers, for example `192.168.1.10`.
- A subnet mask or CIDR prefix separates the network portion from the host portion. For example, `192.168.1.10/24` has 24 network bits and 8 host bits; its subnet mask is `255.255.255.0`.
- The traditional class ranges are Class A (`1–126`), Class B (`128–191`), Class C (`192–223`), Class D (`224–239`, multicast), and Class E (`240–255`, reserved). Modern networks normally use CIDR instead of classful addressing.
- Common private IPv4 ranges are `10.0.0.0/8`, `172.16.0.0/12`, and `192.168.0.0/16`. These addresses are used inside private networks and are not routed directly across the public Internet.
- In a typical IPv4 subnet, the first address is the network address and the last is the broadcast address. They are not assigned to normal hosts.

## Task 2: Networking command practice

Run the following commands in a Linux terminal. The captured output below was collected on 3 September 2026 from a Windows computer because no Linux terminal is available in this workspace. Windows equivalents were used for the captures. Device-specific values (hostname, MAC address, local IP address, gateway, and active connections) are redacted for privacy. Output differs by computer, network, and time.

> I must use only hosts and networks that I own or am authorized to test. The commands below are read-only diagnostics, except that `ping` sends normal ICMP echo requests.

### 1. `ip addr`

```bash
ip addr
```

**What I understood:** This command shows the network interfaces on the machine, their status, MAC addresses, and assigned IPv4/IPv6 addresses. I can use it to identify my active interface and local IP address.

**Actual output (Windows equivalent: `ipconfig /all`):**

```text
Windows IP Configuration

Wireless LAN adapter Wi-Fi:
   Description . . . . . . . . . . : Intel(R) Wireless-AC 9560 160MHz
   Physical Address. . . . . . . . .: [REDACTED]
   DHCP Enabled. . . . . . . . . . .: Yes
   IPv4 Address. . . . . . . . . . .: [REDACTED]
   Subnet Mask . . . . . . . . . . .: 255.255.240.0
   Default Gateway . . . . . . . . . : [REDACTED]
```

### 2. `ip route`

```bash
ip route
```

**What I understood:** This displays the routing table. The line starting with `default via` identifies the default gateway, which is the router used to reach networks outside my local subnet.

**Actual output (Windows equivalent: `route print -4`):**

```text
IPv4 Route Table
Active Routes:
Network Destination        Netmask          Gateway       Interface  Metric
          0.0.0.0          0.0.0.0    [REDACTED]      [REDACTED]     40
    [REDACTED]       255.255.240.0         On-link       [REDACTED]    296
        127.0.0.0        255.0.0.0         On-link         127.0.0.1    331
```

### 3. `ping`

```bash
ping -c 4 8.8.8.8
ping -c 4 google.com
```

**What I understood:** `ping` tests reachability and reports round-trip latency and packet loss. Pinging an IP checks basic network connectivity; pinging a hostname also checks whether DNS name resolution works. Some hosts or firewalls block ICMP, so a failed ping does not always prove that a service is down.

**Actual output (Windows equivalent: `ping -n 4 8.8.8.8`):**

```text
Pinging 8.8.8.8 with 32 bytes of data:
Reply from 8.8.8.8: bytes=32 time=9ms TTL=117
Reply from 8.8.8.8: bytes=32 time=8ms TTL=117
Reply from 8.8.8.8: bytes=32 time=8ms TTL=117
Reply from 8.8.8.8: bytes=32 time=8ms TTL=117

Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)
Minimum = 8ms, Maximum = 9ms, Average = 8ms
```

### 4. `hostname` and `hostname -I`

```bash
hostname
hostname -I
```

**What I understood:** `hostname` prints the computer’s host name. `hostname -I` prints the IP address(es) assigned to the local machine. These commands quickly identify the device during network troubleshooting.

**Actual output (Windows equivalent: `hostname`):**

```text
[REDACTED-HOSTNAME]
```

### 5. `ss`

```bash
ss -tuln
```

**What I understood:** `ss` displays socket information. `-t` selects TCP, `-u` selects UDP, `-l` shows listening sockets, and `-n` keeps addresses and ports numeric. I use it to see which local ports have services waiting for connections.

**Actual output (Windows equivalent: `netstat -ano`; selected listening ports):**

```text
Active Connections

Proto  Local Address          Foreign Address        State           PID
TCP    0.0.0.0:135            0.0.0.0:0              LISTENING       [REDACTED]
TCP    0.0.0.0:445            0.0.0.0:0              LISTENING       4
TCP    0.0.0.0:3306           0.0.0.0:0              LISTENING       [REDACTED]
TCP    127.0.0.1:27017        0.0.0.0:0              LISTENING       [REDACTED]
```

### 6. `nslookup` (DNS lookup)

```bash
nslookup google.com
```

**What I understood:** `nslookup` asks DNS for the IP address associated with a domain name. It helps distinguish a DNS problem from a general connectivity problem.

**Actual output (Windows command: `nslookup google.com`):**

```text
DNS request timed out.
    timeout was 2 seconds.
Server:  UnKnown
Address:  [REDACTED]

DNS request timed out.
    timeout was 2 seconds.
```

**Observation:** The DNS lookup timed out on the configured DNS server during this test. This is a useful troubleshooting result: basic IP connectivity worked (the ping test passed), but the DNS query did not receive a reply.

### 7. `traceroute`

```bash
traceroute google.com
```

**What I understood:** `traceroute` shows the network hops between my computer and a destination. It is useful for locating where a connection may be delayed or stopped. A `*` can simply mean that a router does not reply to traceroute probes.

**Actual output (Windows equivalent: `tracert -d -h 3 google.com`):**

```text
Tracing route to google.com [142.250.205.206]
over a maximum of 3 hops:

  1     5 ms     3 ms     2 ms  [REDACTED-GATEWAY]
  2     2 ms     2 ms     1 ms  [REDACTED]
  3     *        4 ms     4 ms  [REDACTED]

Trace complete.
```

### 8. `curl`

```bash
curl -I https://example.com
```

**What I understood:** `curl -I` sends an HTTP request and shows response headers only. It verifies that DNS, the TCP/HTTPS connection, and the web server response are working. A status such as `200` or `301` shows the server responded successfully.

**Actual output (Windows command: `curl.exe -I --max-time 10 https://example.com`):**

```text
curl: (7) Failed to connect to example.com:443 after 4183 ms: Could not connect to server
```

**Observation:** The HTTPS connection was blocked or unavailable from this environment at the time of testing. This does not necessarily mean that `example.com` is down; a proxy, firewall, or network policy can also cause this error.

## Notes from my practice

- `ip` and `ss` are modern Linux tools. On older systems, `ifconfig` and `netstat` may be available, but they are commonly replaced by `ip` and `ss`.
- `traceroute`, `nslookup`, and `dig` may need installation on a minimal Linux system. On Ubuntu: `sudo apt install traceroute dnsutils`.
- If I use Windows instead of Linux, comparable commands are `ipconfig /all`, `route print`, `ping`, `nslookup`, `tracert`, and `netstat -ano`.

## Submission checklist

-  Created this Markdown file.
-  Added explanations of each networking command.
- Executed Windows-equivalent networking diagnostics and added actual, privacy-redacted output.

