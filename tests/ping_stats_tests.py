import unittest
from ping_stats import PingStats


class TestPingStats(unittest.TestCase):
    def test_initialization(self):
        stats = PingStats()
        self.assertEqual(stats.sent_packets, 0)
        self.assertEqual(stats.received_packets, 0)
        self.assertEqual(stats.round_trip_times, [])

    def test_print_stats_no_packets(self):
        stats = PingStats()
        with self.assertLogs() as cm:
            stats.print_stats()

        self.assertIn('Sent: 0', cm.output[0])
        self.assertIn('Received: 0', cm.output[0])
        self.assertIn('Lost: 0', cm.output[0])
        self.assertIn('Loss percentage: 0.00%', cm.output[0])
        self.assertIn('Min RTT: N/A', cm.output[0])
        self.assertIn('Max RTT: N/A', cm.output[0])
        self.assertIn('Avg RTT: N/A', cm.output[0])
        self.assertIn('StdDev RTT: N/A', cm.output[0])

    def test_print_stats_with_packets(self):
        stats = PingStats()
        stats.sent_packets = 10
        stats.received_packets = 7
        stats.round_trip_times = [1.2, 3.4, 2.5, 5.0, 4.2, 1.8, 3.0]

        with self.assertLogs() as cm:
            stats.print_stats()

        self.assertIn('Sent: 10', cm.output[0])
        self.assertIn('Received: 7', cm.output[0])
        self.assertIn('Lost: 3', cm.output[0])
        self.assertIn('Loss percentage: 30.00%', cm.output[0])
        self.assertIn('Min RTT: 1.20ms', cm.output[0])
        self.assertIn('Max RTT: 5.00ms', cm.output[0])
        self.assertIn('Avg RTT: 2.71ms', cm.output[0])
        self.assertIn('StdDev RTT: 1.28ms', cm.output[0])


if __name__ == '__main__':
    unittest.main()
