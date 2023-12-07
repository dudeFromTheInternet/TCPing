import unittest
from unittest.mock import patch
from io import StringIO
from ping_stats import PingStats


class TestPingStats(unittest.TestCase):
    def test_initialization(self):
        target = 'example.com'
        stats = PingStats(target)
        self.assertEqual(stats.target, target)
        self.assertEqual(stats.sent_packets, 0)
        self.assertEqual(stats.received_packets, 0)
        self.assertEqual(stats.round_trip_times, [])

    def test_print_stats_no_packets(self):
        target = 'example.com'
        stats = PingStats(target)

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            stats.print_stats()

        expected_output = (
            f'\n--- Ping statistics for {target} ---\n'
            'Sent: 0, Received: 0, Lost: 0, Loss percentage: 0.00%\n'
            'Min RTT: N/A, Max RTT: N/A, Avg RTT: N/A, StdDev RTT: N/A\n'
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_print_stats_with_packets(self):
        target = 'example.com'
        stats = PingStats(target)
        stats.sent_packets = 10
        stats.received_packets = 7
        stats.round_trip_times = [1.2, 3.4, 2.5, 5.0, 4.2, 1.8, 3.0]

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            stats.print_stats()

        expected_output = (
            f'\n--- Ping statistics for {target} ---\n'
            'Sent: 10, Received: 7, Lost: 3, Loss percentage: 30.00%\n'
            'Min RTT: 1.20ms, Max RTT: 5.00ms, Avg RTT: 2.71ms, StdDev RTT: 1.28ms\n'
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)


if __name__ == '__main__':
    unittest.main()
