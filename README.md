# python-port-scanner
Python TCP connect port scanner with a sequential and a multithreaded version, tested on a home lab
# Python Port Scanner

A TCP connect port scanner written in Python, built to learn how port scanning works under the hood. It comes in two versions: a simple sequential scanner and a faster multithreaded one.

> **Disclaimer:** This project is for educational use only. Only scan systems you own or have explicit written permission to test. Scanning systems without authorization may be illegal.

## What it does

The scanner tries to open a TCP connection to each port in the range 1-1024 on a target host. If the connection succeeds, the port is reported as open. This is the same technique as a `nmap -sT` (TCP connect) scan.

## How it works

A TCP connection begins with a three-way handshake (SYN, SYN-ACK, ACK). Python's built-in `socket` library performs the handshake for us:

- `connect_ex()` attempts the connection and returns `0` if it succeeds (port open).
- A closed port refuses the connection, while a filtered port (blocked by a firewall) usually just times out, so the scanner reports both as "closed or filtered".
- A 1-second timeout stops the script from hanging on ports that silently drop packets.

## The two versions

| File | Approach | Notes |
|------|----------|-------|
| `scanner.py` | Sequential: checks one port at a time | Simple and easy to follow, but slow |
| `scanner_threaded.py` | Multithreaded: 100 worker threads via `ThreadPoolExecutor` | Checks many ports in parallel |

Most of a scan is spent waiting for replies, so running many checks at once makes a big difference.

## Requirements

- Python 3.8 or newer
- No third-party packages (standard library only)

## Usage

1. Open the script and set `target` to the IP address you are authorized to scan:

   ```python
   target = "TARGET_IP"
   ```

2. Run it:

   ```bash
   python scanner.py
   # or
   python scanner_threaded.py
   ```

## Example output

Scan of an intentionally vulnerable lab VM (Metasploitable 2) on an isolated host-only network:

```
Port 21 is open
Port 22 is open
Port 23 is open
Port 25 is open
...
Scan finished in X.X seconds
```

<!-- TODO: replace the example above with your real full output from scanner_threaded.py -->

## Performance comparison

| Version | Ports scanned | Time |
|---------|---------------|------|
| `scanner.py` (sequential) | 1-1024 | TODO |
| `scanner_threaded.py` (100 threads) | 1-1024 | TODO |

<!-- TODO: fill in your measured times -->

## What I learned

- How the TCP three-way handshake works and how a connect scan uses it
- The difference between open, closed and filtered ports
- How sockets, functions and loops work in Python
- Why scans are slow when sequential, and how threading speeds them up
- How to validate my results by comparing them with nmap output

## Lab setup

- Target: Metasploitable 2 running in VMware on a host-only network
- Scanner: Python 3 (Anaconda) run from VS Code on the host machine

## Possible improvements

- Take the target and port range as command-line arguments (`argparse`)
- Banner grabbing to identify the service on each open port
- Service name lookup (e.g. 21 -> FTP)
- Export results to a file or HTML report



