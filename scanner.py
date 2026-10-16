"""
Basic TCP connect port scanner.
Scans ports 1-1024 on a target host and prints the open ones.

For educational use only, on systems you own or have
explicit permission to test.
"""
import socket

target = "TARGET_IP"   # Metasploitable 2 lab VM or any other host you have permission to scan


def scan_port(target, port):
    """Return True if the TCP port accepts a connection."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)   # don't hang on ports that silently drop packets
    result = s.connect_ex((target, port))   # 0 means connected
    s.close()
    return result == 0


# range() stops before its second number, so 1025 includes port 1024
for port in range(1, 1025):
    if scan_port(target, port):
        print(f"Port {port} is open")