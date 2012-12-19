#! /usr/bin/env python

"""
esmbc generate
~~~~~~~~~~~~~~

Generates the json data file for ship volumes from the CCP database dump.

:copyright: (c) 2012 Stuart Baker
:license: GNU GPL Version 3, see LICENSE

"""

import pymysql
import json

def get_child_groups(cursor, parent_group):
    """Returns a tuple of all the child market group ids"""
    sqlselect = "select marketGroupID"
    sqlfrom = "from invMarketGroups"
    sqlwhere = "where parentGroupID={0}".format(parent_group)

    cursor.execute('{0} {1} {2}'.format(sqlselect, sqlfrom, sqlwhere))
    children = cursor.fetchall()

    for child in children:
        children += get_child_groups(child[0])

    return children

def get_ship_volumes(cursor, group_ids):
    """Returns a tuple of the ship names and volumes in the specified groups"""
    ship_volumes = ()
    for group_id in group_ids:
        sqlselect = "select typeName, volume"
        sqlfrom = "from invTypes"
        sqlwhere = "where marketGroupID={0}".format(group_id[0])
        sqlwhere = "{0} and published=1".format(sqlwhere)
        cursor.execute('{0} {1} {2}'.format(sqlselect, sqlfrom, sqlwhere))
        ship_volumes += cursor.fetchall()

    return ship_volumes

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
    connection = pymysql.connect(host='localhost',
                             unix_socket='/var/run/mysqld/mysqld.sock',
                             user='root',
                             passwd='',
                             db='eve')

    cursor = connection.cursor()

    market_group_id = 4

    group_ids = get_child_groups(cursor, market_group_id)
    ship_volumes = get_ship_volumes(cursor, group_ids)

    ship_dict = dict_convert(ship_volumes)

    print('{0}'.format(json_convert(ship_dict)))

    cursor.close()
    connection.close()
