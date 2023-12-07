import statistics


class PingStats:
    def __init__(self, target):
        self.target = target
        self.sent_packets = 0
        self.received_packets = 0
        self.round_trip_times = []

    def print_stats(self):
        print(f'\n--- Ping statistics for {self.target} ---')
        print(
            f'Sent: {self.sent_packets}, Received: {self.received_packets}, '
            f'Lost: {self.sent_packets - self.received_packets}, '
            f'Loss percentage: {((self.sent_packets - self.received_packets) / self.sent_packets) * 100:.2f}%')

        if self.received_packets > 0:
            print(f'Min RTT: {min(self.round_trip_times):.2f}ms, '
                  f'Max RTT: {max(self.round_trip_times):.2f}ms, '
                  f'Avg RTT: {statistics.mean(self.round_trip_times):.2f}ms, '
                  f'StdDev RTT: '
                  f'{statistics.stdev(self.round_trip_times):.2f}ms')
