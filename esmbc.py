#!/usr/bin/env python

import sys
import json
import os

def load_ship_dict(filename):
    if os.path.exists(filename):
        with open(filename, 'rt') as esmbc_data:
            return json.load(esmbc_data)
    else:
        sys.stderr.write('Unable to load {0} data file \n'.format(filename))
        sys.exit()

def build_ship_table(ship_counts, ship_dict):
    ship_table = {}
    for ship, count in ship_counts.items():
        if ship in ship_dict:
            ship_table[ship] = int(ship_dict[ship]) * int(count)
        else:
            sys.stderr.write('{0} is not a valid ship'.format(ship))

    return ship_table

def print_table(ship_table):
    total = 0
    for ship, subtotal in ship_table.items():
        total += subtotal
        print('{0:25} ==> {1:10}m3'.format(ship, subtotal))

    print('{0:40}m3'.format(total))

if __name__ == "__main__":

    ship_dict = load_ship_dict('esmbc_data.json')

    ship_counts = {}
    for arg in sys.argv[1:]:
        ship, count = arg.split(':', maxsplit=1)
        ship_counts[ship] = count

    ship_table = build_ship_table(ship_counts, ship_dict)

    print_table(ship_table)
