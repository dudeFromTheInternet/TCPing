import unittest
from unittest.mock import patch, MagicMock
from tcping import TCPing


class TestTCPing(unittest.TestCase):
    @patch('tcping.socket.gethostbyname', return_value='127.0.0.1')
    @patch('tcping.sr1',
           return_value=MagicMock(haslayer=MagicMock(return_value=True),
                                  TCP=MagicMock(flags=18)))
    @patch('tcping.time.sleep')
    def test_run(self, mock_sleep, mock_sr1, mock_gethostbyname):
        tcping = TCPing('example.com', 80, timeout=5, num_pings=3, interval=1)
        tcping.run()

        self.assertEqual(tcping.stats.sent_packets, 3)
        self.assertEqual(tcping.stats.received_packets, 3)
        self.assertGreaterEqual(len(tcping.stats.round_trip_times), 3)
        mock_gethostbyname.assert_called_once_with('example.com')
        mock_sr1.assert_called()
        mock_sleep.assert_called()


if __name__ == '__main__':
    unittest.main()
