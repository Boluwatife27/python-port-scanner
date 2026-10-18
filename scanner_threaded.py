"""
Multithreaded TCP connect port scanner with command-line options.

Usage:
    python scanner_threaded.py TARGET [-s START] [-e END] [-t THREADS]

For educational use only, on systems you own or have
explicit permission to test.
"""
import argparse
import socket
import time
from concurrent.futures import ThreadPoolExecutor


def scan_port(target, port):
    """Return (port, True) if the TCP port accepts a connection."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)   # don't hang on ports that silently drop packets
    result = s.connect_ex((target, port))   # 0 means connected
    s.close()
    return port, result == 0


def main():
    parser = argparse.ArgumentParser(
        description="Multithreaded TCP connect port scanner"
    )
    parser.add_argument("target", help="IP address or hostname to scan")
    parser.add_argument("-s", "--start", type=int, default=1,
                        help="first port to scan (default: 1)")
    parser.add_argument("-e", "--end", type=int, default=1024,
                        help="last port to scan (default: 1024)")
    parser.add_argument("-t", "--threads", type=int, default=100,
                        help="number of worker threads (default: 100)")
    args = parser.parse_args()

    if not (1 <= args.start <= args.end <= 65535):
        parser.error("ports must satisfy 1 <= start <= end <= 65535")

    start_time = time.time()
    ports = range(args.start, args.end + 1)   # +1 to include the end port

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        results = executor.map(lambda p: scan_port(args.target, p), ports)

    for port, is_open in results:
        if is_open:
            print(f"Port {port} is open")

    print(f"Scan finished in {time.time() - start_time:.1f} seconds")


if __name__ == "__main__":
    main()
