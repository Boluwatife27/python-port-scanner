"""
Multithreaded TCP connect port scanner.
Scans ports 1-1024 on a target host using a pool of worker threads
and prints the open ones.

For educational use only, on systems you own or have
explicit permission to test.
"""
import socket
import time
from concurrent.futures import ThreadPoolExecutor

target = "TARGET_IP"   # Metasploitable 2 lab VM or any other host you have permission to scan


def scan_port(port):
    """Return (port, True) if the TCP port accepts a connection."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((target, port))   # 0 means connected
    s.close()
    return port, result == 0


start = time.time()

# Workers check ports in parallel; map() keeps results in port order
with ThreadPoolExecutor(max_workers=100) as executor:
    results = executor.map(scan_port, range(1, 1025))

for port, is_open in results:
    if is_open:
        print(f"Port {port} is open")

print(f"Scan finished in {time.time() - start:.1f} seconds")