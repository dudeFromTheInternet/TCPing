from scapy.layers.inet import IP, TCP, sr1
import time
import argparse
import socket
from ping_stats import PingStats


class TCPing:
    def __init__(self, host, port, timeout=5, num_pings=None, interval=1):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.num_pings = num_pings
        self.interval = interval
        self.stats = PingStats()

    def resolve_host(self):
        try:
            ip_address = socket.gethostbyname(self.host)
            return ip_address
        except socket.gaierror:
            return self.host

    def parse_arguments(self):
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

        self.host = args.host
        self.port = args.port
        self.num_pings = args.num_pings
        self.timeout = args.timeout
        self.interval = args.interval

    def run(self):
        try:
            self.parse_arguments()
            ip_address = self.resolve_host()
            while self.num_pings is None or self.num_pings > 0:
                start_time = time.time()

                ip_packet = IP(dst=ip_address, proto=4)
                tcp_packet = TCP(dport=self.port, flags="S")

                response_packet = sr1(ip_packet / tcp_packet,
                                      timeout=self.timeout,
                                      verbose=0)

                end_time = time.time()
                elapsed_time = end_time - start_time

                if response_packet and response_packet.haslayer(TCP) and \
                        response_packet[TCP].flags == 0x12:
                    print(f'{ip_address}:{self.port} is reachable. Time={elapsed_time:.2f}ms')
                    self.stats.received_packets += 1
                    self.stats.round_trip_times.append(elapsed_time)
                else:
                    print(f'{ip_address}:{self.port} is not reachable.')

                self.stats.sent_packets += 1

                if self.num_pings is not None:
                    self.num_pings -= 1

                time.sleep(self.interval)

        except KeyboardInterrupt:
            pass

        finally:
            self.stats.print_stats()


if __name__ == "__main__":
    tcping = TCPing('', 0)
    tcping.run()
