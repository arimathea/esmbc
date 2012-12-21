#!/usr/bin/env python
"""
esmbc
~~~~~

Calculates total ship volume of supplied ships and quantity pairs.

:copyright: (c) 2012 Stuart Baker
:license: GNU GPL Version 3, see LICENSE

"""
import sys
import json
import os

def load_ship_dict(filename):
    """Loads the ship volume dictionary from a JSON file and returns it"""
    if os.path.exists(filename):
        with open(filename, 'rt') as esmbc_data:
            return json.load(esmbc_data)
    else:
        sys.stderr.write('Unable to load {0} data file \n'.format(filename))
        sys.exit()

def parse_arguments(args):
    """Parses the ship count pairs and returns a ship count dict"""
    if not args:
        sys.stderr.write('Please supply some ship:count pairs as arguments\n')
        sys.exit()

    ship_counts = {}
    for arg in args:
        try:
            ship, count = arg.split(':', maxsplit=1)
        except ValueError:
            sys.stderr.write('Arguments need to be in format:  ship:count\n')
            sys.exit()
        else:
            ship_counts[ship] = count

    return ship_counts

def build_ship_table(ship_counts, ship_dict):
    """Builds and returns a dict of ships and subtotal of their volumes"""
    ship_table = {}
    for ship, count in ship_counts.items():
        if ship not in ship_dict:
            sys.stderr.write('{0} is not a valid ship \n'.format(ship))
            sys.exit()

        try:
            ship_table[ship] = int(ship_dict[ship]) * int(count)
        except ValueError:
            sys.stderr.write('Invalid ship count number \n')
            sys.exit()

    return ship_table

def print_table(ship_table):
    """Prints the supplied ship volume table and total volume"""
    total = 0
    for ship, subtotal in ship_table.items():
        total += subtotal
        print('{0:25} ==> {1:10}m3'.format(ship, subtotal))

    print('{0:40}m3'.format(total))

if __name__ == "__main__":
    esmbc_dir = os.path.dirname(os.path.realpath(__file__))
    data_file = os.path.join(esmbc_dir, 'esmbc_data.json')

    ship_dict = load_ship_dict(data_file)
    ship_counts = parse_arguments(sys.argv[1:])
    ship_table = build_ship_table(ship_counts, ship_dict)
    print_table(ship_table)
