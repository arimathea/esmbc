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
import sys

def get_child_groups(cursor, parent_group):
    """Returns a tuple of all the child market group ids"""
    sqlselect = "select marketGroupID"
    sqlfrom = "from invMarketGroups"
    sqlwhere = "where parentGroupID={0}".format(parent_group)

    cursor.execute('{0} {1} {2}'.format(sqlselect, sqlfrom, sqlwhere))
    children = cursor.fetchall()

    for child in children:
        children += get_child_groups(cursor, child[0])

    return children

def get_ship_volumes(cursor, group_ids):
    """Returns a tuple of the ship names and volumes in the specified groups"""

    sqlselect = "select typeName, volume"
    sqlfrom = "from invTypes"
    sqlwhere = "where published=1"
    sqlwhere = "{0} and marketGroupID={1}".format(sqlwhere, group_ids[0][0])

    for group_id in group_ids[1:]:
        sqlwhere = "{0} OR marketGroupID={1}".format(sqlwhere, group_id[0])

    cursor.execute('{0} {1} {2}'.format(sqlselect, sqlfrom, sqlwhere))
    return cursor.fetchall()

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

if __name__ == "__main__":
    connection = sqlite3.connect(sys.argv[1])

    cursor = connection.cursor()

    # Market group id of the parent ship market group
    market_group_id = 4

    group_ids = get_child_groups(cursor, market_group_id)
    ship_volumes = get_ship_volumes(cursor, group_ids)

    ship_dict = dict_convert(ship_volumes)

    print('{0}'.format(json_convert(ship_dict)))

    cursor.close()
    connection.close()
