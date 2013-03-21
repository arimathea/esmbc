#!/usr/bin/env python
"""
cli
~~~~~

Cli program that calculates total ship volume of supplied ships and quantity
pairs.

:copyright: (c) 2013 Stuart Baker
:license: GNU GPL Version 3, see LICENSE

"""
import sys
import json
import os
import argparse


def load_volumes(filename):
    """Loads the ship volume dictionary from a JSON file and returns it"""
    if not os.path.exists(filename):
        raise FileNotFoundError('Unable to load {}'.format(filename))

    with open(filename, 'rt') as esmbc_data:
        return json.load(esmbc_data)


def parse_ship_pairs(pairs):
    """Parses the ship count pairs and returns a ship count dict"""
    if not pairs:
        return None

    ship_counts = {}
    for pair in pairs:
        try:
            ship, count = pair.split(':', maxsplit=1)
        except ValueError:
            return None
        else:
            ship_counts[str.lower(ship)] = count

    return ship_counts


def calculate_volume_totals(ship_counts, ship_volumes):
    """Builds and returns a dict of ships and subtotal of their volumes"""
    if not ship_counts:
        return None

    volume_totals = {}
    for ship, count in ship_counts.items():
        if ship not in ship_volumes:
            return None
        try:
            volume_totals[ship] = int(ship_volumes[ship]) * int(count)
        except ValueError:
            return None

    return volume_totals


def format_table(volume_totals):
    """Prints the supplied ship volume table and total volume"""
    total = 0
    table = ''

    if not volume_totals:
        return None

    for ship, subtotal in volume_totals.items():
        total += subtotal
        table = '{}{}: {:,}m3\n'.format(table, pretty_ship(ship), subtotal)

    table = '{}Total: {:,}m3'.format(table, total)
    return table


def pretty_ship(ship):
    """Returns a ship name with underscores replaced with whitespace and the
    the first letter of each word in uppercase
    """
    pretty = ship.replace('_', ' ')
    pretty = pretty.title()
    return pretty


def main():
    esmbc_dir = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(esmbc_dir, 'ships.json')
    parser = argparse.ArgumentParser(prog='esmbc',
        description='Calculates the total volume of supplied ships.')
    parser.add_argument('ships', nargs='+',
                        help='ships in the format ship:quantity')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 0.2.0')
    args = parser.parse_args()

    try:
        ship_volumes = load_volumes(filename)
    except FileNotFoundError as error:
        sys.stderr.write('{}\n'.format(error))
        sys.exit()

    ship_counts = parse_ship_pairs(args.ships)
    if not ship_counts:
        parser.print_help()
        sys.exit()

    volume_totals = calculate_volume_totals(ship_counts, ship_volumes)
    if not volume_totals:
        parser.print_help()
        sys.exit()

    total = format_table(volume_totals)
    if not total:
        parser.print_help()
        sys.exit()

    print('{}'.format(total))
    sys.exit()
