from scapy.layers.inet import IP, TCP, sr1
import time
import argparse
import statistics
import socket


class PingStats:
    def __init__(self):
        self.sent_packets = 0
        self.received_packets = 0
        self.round_trip_times = []


def resolve_host(host):
    try:
        ip_address = socket.gethostbyname(host)
        return ip_address
    except socket.gaierror:
        return host


def tcping_synack(host, port, timeout=5, num_pings=None, interval=1):
    stats = PingStats()

    try:
        ip_address = resolve_host(host)
        while num_pings is None or num_pings > 0:
            start_time = time.time()

            ip_packet = IP(dst=ip_address, proto=4)
            tcp_packet = TCP(dport=port, flags="S")

            response_packet = sr1(ip_packet / tcp_packet, timeout=timeout,
                                  verbose=0)

            end_time = time.time()
            elapsed_time = end_time - start_time

            if response_packet and response_packet.haslayer(TCP) and \
                    response_packet[TCP].flags == 18:
                print(f'{ip_address}:{port} is reachable. Time={elapsed_time:.2f}ms')
                stats.received_packets += 1
                stats.round_trip_times.append(elapsed_time)
            else:
                print(f'{ip_address}:{port} is not reachable.')

            stats.sent_packets += 1

            if num_pings is not None:
                num_pings -= 1

            time.sleep(interval)

    except KeyboardInterrupt:
        pass

    finally:
        print('\n--- Ping statistics ---')
        print(
            f'Sent: {stats.sent_packets}, Received: {stats.received_packets}, '
            f'Lost: {stats.sent_packets - stats.received_packets}, '
            f'Loss percentage: {((stats.sent_packets - stats.received_packets) / stats.sent_packets) * 100:.2f}%')

        if stats.received_packets > 0:
            print(f'Min RTT: {min(stats.round_trip_times):.2f}ms, '
                  f'Max RTT: {max(stats.round_trip_times):.2f}ms, '
                  f'Avg RTT: {statistics.mean(stats.round_trip_times):.2f}ms, '
                  f'StdDev RTT: '
                  f'{statistics.stdev(stats.round_trip_times):.2f}ms')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Check TCP connectivity using SYN/ACK.')
    parser.add_argument('host', type=str, help='Target host to check.')
    parser.add_argument('port', type=int, help='Port to check.')
    parser.add_argument('-n', '--num-pings', type=int, default=None,
                        help='Number of pings to send.')
    parser.add_argument('-t', '--timeout', type=int, default=5,
                        help='Timeout for each ping.')
    parser.add_argument('-i', '--interval', type=int, default=1,
                        help='Interval between pings in seconds.')
    args = parser.parse_args()

    tcping_synack(args.host, args.port, timeout=args.timeout,
                  num_pings=args.num_pings, interval=args.interval)
