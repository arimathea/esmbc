#!C/usr/bin/env python
"""
test_esmbc
~~~~~~~~~~

Test file for esmbc

:copyright: (c) 2012 Stuart Baker
:license: GNU GPL Version 3, see LICENSE

"""
import unittest
import os
import esmbc.cli as esmbc

class TestEsmbc(unittest.TestCase):

    def test_load_ship_dict(self):
        # data/test_ships.json:
        # {
        #     "zephyr":5000.0
        # }
        volumes = {'zephyr': 5000.0}
        esmbc_dir = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(esmbc_dir, 'test_ships.json')

        self.assertEqual(esmbc.load_volumes(filename), volumes)
        self.assertRaises(FileNotFoundError, esmbc.load_volumes, 'foo.json')

    def test_parse_ship_pairs(self):
        pairs = ['foo:1', 'bar:2']
        counts = {'foo' : '1', 'bar' : '2'}

        self.assertDictEqual(counts, esmbc.parse_ship_pairs(pairs))
        self.assertRaisesRegex(ValueError,
                               'Invalid argument format',
                               esmbc.parse_ship_pairs, 'foo')
        self.assertRaisesRegex(Exception,
                               'No ship and count pairs were supplied',
                               esmbc.parse_ship_pairs, [])

    def test_calculate_volume_totals(self):
        volumes = {'zephyr': 5000.0}
        counts = {'zephyr' : '2'}
        totals = {'zephyr' : 10000}

        self.assertDictEqual(esmbc.calculate_volume_totals(counts, volumes),
                              totals)
        self.assertRaisesRegex(Exception, 'foo is not a valid ship',
                               esmbc.calculate_volume_totals,
                               {'foo' : '1'}, volumes)
        self.assertRaisesRegex(Exception, 'No ship counts were supplied',
                               esmbc.calculate_volume_totals,
                               {}, volumes)


        self.assertRaises(ValueError, esmbc.calculate_volume_totals,
                         {'zephyr' : 'bar'}, volumes)

    def test_format_table(self):
        totals = {'zephyr' : 10000}
        table = '     10000m3 (zephyr)\n'
        table = '{0}     10000m3'.format(table)

        self.assertEqual(esmbc.format_table(totals), table)
        self.assertRaisesRegex(Exception, 'No volume totals were supplied',
                               esmbc.format_table, {})

if __name__ == "__main__":
    unittest.main()
