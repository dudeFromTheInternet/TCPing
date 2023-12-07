from scapy.layers.inet import IP, TCP, sr1
import time
import argparse
import socket
from ping_stats import PingStats


class TCPing:
    def __init__(self, targets, timeout=5, num_pings=None, interval=1):
        self.targets = targets
        self.timeout = timeout
        self.num_pings = num_pings
        self.interval = interval
        self.stats = {target: PingStats(target) for target in self.targets}

    def resolve_host(self, host):
        try:
            ip_address = socket.gethostbyname(host)
            return ip_address
        except socket.gaierror:
            return host

    def parse_arguments(self):
        parser = argparse.ArgumentParser(
            description='Check TCP connectivity using SYN/ACK.')
        parser.add_argument('targets', nargs='+', type=str, help='Target '
                                                                 'hosts and '
                                                                 'ports to '
                                                                 'check. '
                                                                 'Format: '
                                                                 'host:port')
        parser.add_argument('-n', '--num-pings', type=int, default=None,
                            help='Number of pings to send.')
        parser.add_argument('-t', '--timeout', type=int, default=5,
                            help='Timeout for each ping.')
        parser.add_argument('-i', '--interval', type=int, default=1,
                            help='Interval between pings in seconds.')
        args = parser.parse_args()

        self.targets = args.targets
        self.num_pings = args.num_pings
        self.timeout = args.timeout
        self.interval = args.interval
        self.stats = {target: PingStats(target) for target in self.targets}

    def run(self):
        try:
            self.parse_arguments()
            while self.num_pings is None or self.num_pings > 0:
                for target in self.targets:
                    host, port = target.split(':')
                    ip_address = self.resolve_host(host)
                    start_time = time.time()

                    ip_packet = IP(dst=ip_address)
                    tcp_packet = TCP(dport=int(port), flags="S")

                    response_packet = sr1(ip_packet / tcp_packet,
                                          timeout=self.timeout,
                                          verbose=0)

                    end_time = time.time()
                    elapsed_time = end_time - start_time

                    if response_packet:
                        if response_packet.haslayer(TCP):
                            if response_packet[TCP].flags == 18:
                                print(f'{ip_address}:{port} is reachable. '
                                      f'Time={elapsed_time:.2f}ms')
                                self.stats[target].received_packets += 1
                                self.stats[target].round_trip_times.append(
                                    elapsed_time)
                            elif response_packet[TCP].flags == 0x14:
                                print(
                                    f"Port {port} on {ip_address} is closed")
                            elif response_packet[TCP].flags == 0x11:
                                print(f"Port {port} on {ip_address} is open, "
                                      f"no response")
                            elif response_packet[TCP].flags == 0x10 or \
                                    response_packet[TCP].flags == 0x02:
                                print(f"Port {port} on {ip_address} is open "
                                      f"and reset")
                            elif response_packet[TCP].flags == 0x04:
                                print(
                                    f"Port {port} on {ip_address} is closed")
                            elif response_packet[TCP].flags & 0x01:
                                print(
                                    f"Received FIN from {ip_address}:{port}")
                            elif response_packet[TCP].flags & 0x11:
                                print(
                                    f"Received FIN-ACK from {ip_address}:{port}")
                            elif response_packet[TCP].flags & 0x08:
                                print(
                                    f"Received PSH from {ip_address}:{port}")
                            elif response_packet[TCP].flags & 0x18:
                                print(
                                    f"Received PSH-ACK from {ip_address}:{port}")
                            else:
                                print(f"Received a response from"
                                      f"{ip_address}:{port}, "
                                      f"but with unexpected TCP flags: {hex(response_packet[TCP].flags)}")
                        else:
                            print(
                                f"Unexpected response without TCP layer from "
                                f"{ip_address}:{port}")
                    else:
                        print(f'{ip_address}:{port} is not reachable.')

                    self.stats[target].sent_packets += 1

                    if self.num_pings is not None:
                        self.num_pings -= 1

                    time.sleep(self.interval)

        except KeyboardInterrupt:
            pass

        finally:
            for target in self.targets:
                self.stats[target].print_stats()


if __name__ == "__main__":
    tcping = TCPing([])
    tcping.run()
