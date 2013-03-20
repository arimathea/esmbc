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
        raise FileNotFoundError('Unable to load {0}'.format(filename))

    with open(filename, 'rt') as esmbc_data:
        return json.load(esmbc_data)


def parse_ship_pairs(pairs):
    """Parses the ship count pairs and returns a ship count dict"""
    if not pairs:
        raise Exception('No ship and count pairs were supplied')

    ship_counts = {}
    for pair in pairs:
        try:
            ship, count = pair.split(':', maxsplit=1)
        except ValueError:
            raise ValueError('Invalid argument format')
        except:
            raise Exception('Unknown error occured while parsing ship pairs')
        else:
            ship_counts[ship] = count

    return ship_counts


def calculate_volume_totals(ship_counts, ship_volumes):
    """Builds and returns a dict of ships and subtotal of their volumes"""
    if not ship_counts:
        raise Exception('No ship counts were supplied')

    volume_totals = {}
    for ship, count in ship_counts.items():
        if ship not in ship_volumes:
            raise Exception('{0} is not a valid ship'.format(ship))

        try:
            volume_totals[ship] = int(ship_volumes[ship]) * int(count)
        except ValueError:
            raise ValueError('The supplied volume or count is not a number')
        except:
            raise Exception('Unknown error occured while calculating volumes')

    return volume_totals


def format_table(volume_totals):
    """Prints the supplied ship volume table and total volume"""
    total = 0
    table = ''

    if not volume_totals:
        raise Exception('No volume totals were supplied')

    for ship, subtotal in volume_totals.items():
        total += subtotal
        table = '{0}{1:10}m3 ({2})\n'.format(table, subtotal, ship)

    table = '{0}{1:10}m3'.format(table, total)
    return table


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
        ship_counts = parse_ship_pairs(args.ships)
        volume_totals = calculate_volume_totals(ship_counts, ship_volumes)
        total = format_table(volume_totals)
    except FileNotFoundError as error:
        sys.stderr.write('{0}\n'.format(error))
    except ValueError as error:
        sys.stderr.write('{0}\n'.format(error))
    except Exception as error:
        sys.stderr.write('{0}\n'.format(error))
    else:
        print('{0}'.format(total))
    finally:
        sys.exit()
