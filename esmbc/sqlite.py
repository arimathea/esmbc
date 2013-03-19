#! /usr/bin/env python

"""
sqlite
~~~~~~~~~~~~~~

Generates the json data file for ship volumes from a sqlite conversion of the
CCP database dump.

:copyright: (c) 2013 Stuart Baker
:license: GNU GPL Version 3, see LICENSE

"""

import sqlite3
import json
import argparse

def get_child_groups(cur, parent_group):
    """Returns a tuple of all the child market group ids"""
    sqlselect = "select marketGroupID"
    sqlfrom = "from invMarketGroups"
    sqlwhere = "where parentGroupID={0}".format(parent_group)

    cur.execute('{0} {1} {2}'.format(sqlselect, sqlfrom, sqlwhere))
    children = cur.fetchall()

    for child in children:
        children += get_child_groups(cur, child[0])

    return children

def get_ship_volumes(cur, group_ids):
    """Returns a tuple of the ship names and volumes in the specified groups"""

    sqlselect = "select typeName, volume"
    sqlfrom = "from invTypes"
    sqlwhere = "where published=1"
    sqlwhere = "{0} and marketGroupID={1}".format(sqlwhere, group_ids[0][0])

    for group_id in group_ids[1:]:
        sqlwhere = "{0} OR marketGroupID={1}".format(sqlwhere, group_id[0])

    cur.execute('{0} {1} {2}'.format(sqlselect, sqlfrom, sqlwhere))
    return cur.fetchall()

def dict_convert(ship_volumes):
    """Converts and returns the supplied ship volume tuple in dictionary form"""
    ship_dict = {}
    for ship, volume in ship_volumes:
        ship = ship.replace(' ', '')
        ship = ship.replace('-', '')
        ship = ship.lower()
        ship_dict[ship] = volume

    return ship_dict

def json_convert(ship_dict):
    """Return a json string of the supplied ship volume dictionary"""
    ship_json = json.dumps(ship_dict,
                           indent=4,
                           sort_keys=True,
                           separators=(',',':'))
    return ship_json


def main():
    # This is the group id of the ship market group which is a parent to all
    # other market groups that contain ships
    market_group_id = 4

    parser = argparse.ArgumentParser(description='Generate esmbc ship data.')
    parser.add_argument('database',
                        help='sqlite3 database file of ccp data dump')
    args = parser.parse_args()

    con = sqlite3.connect(args.database)
    cur = con.cursor()

    group_ids = get_child_groups(cur, market_group_id)
    ship_volumes = get_ship_volumes(cur, group_ids)
    ship_dict = dict_convert(ship_volumes)
    print('{0}'.format(json_convert(ship_dict)))

    cur.close()
    con.close()


if __name__ == "__main__":
    main()
