import unittest
from unittest.mock import patch
from ping_stats import PingStats
from tcping import TCPing


class TestTCPing(unittest.TestCase):
    def test_initialization(self):
        tcping = TCPing(['example.com:80', 'google.com:443'])
        self.assertEqual(tcping.targets, ['example.com:80', 'google.com:443'])
        self.assertEqual(tcping.timeout, 5)
        self.assertIsNone(tcping.num_pings)
        self.assertEqual(tcping.interval, 1)

    def test_parse_arguments(self):
        args = ['example.com:80', 'google.com:443', '-n', '10', '-t', '3',
                '-i', '2']
        with patch('sys.argv', ['tcping.py'] + args):
            tcping = TCPing([])
            tcping.parse_arguments()

        self.assertEqual(tcping.targets, ['example.com:80', 'google.com:443'])
        self.assertEqual(tcping.num_pings, 10)
        self.assertEqual(tcping.timeout, 3)
        self.assertEqual(tcping.interval, 2)

    def test_run_method(self):
        targets = ['example.com:80', 'google.com:443']
        with patch('sys.argv', ['tcping.py'] + targets), \
                patch('builtins.print') as mock_print:
            tcping = TCPing([])
            tcping.run()

        for target in targets:
            self.assertIn(target, tcping.stats)
            self.assertIsInstance(tcping.stats[target], PingStats)
            self.assertTrue(tcping.stats[target].print_stats.called)

    def test_run_method_with_keyboard_interrupt(self):
        with patch('sys.argv', ['tcping.py', 'example.com:80']), \
                patch('builtins.print') as mock_print:
            tcping = TCPing([])
            with self.assertRaises(KeyboardInterrupt):
                tcping.run()

        self.assertIn('example.com:80', tcping.stats)
        self.assertIsInstance(tcping.stats['example.com:80'], PingStats)
        self.assertTrue(tcping.stats['example.com:80'].print_stats.called)


if __name__ == '__main__':
    unittest.main()
