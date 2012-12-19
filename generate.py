#! /usr/bin/env python

import pymysql
import json

connection = pymysql.connect(host='localhost',
                             unix_socket='/var/run/mysqld/mysqld.sock',
                             user='root',
                             passwd='',
                             db='eve')

cursor = connection.cursor()

parent = 4

def get_child_groups(parent):
    sqlselect = "select marketGroupID"
    sqlfrom = "from invMarketGroups"
    sqlwhere = "where parentGroupID={0}".format(parent)

    cursor.execute('{0} {1} {2}'.format(sqlselect, sqlfrom, sqlwhere))
    children = cursor.fetchall()

    for child in children:
        children += get_child_groups(child[0])

    return children

def get_invtypes(groups):
    invtypes = ()
    for group in groups:
        sqlselect = "select typeName, volume"
        sqlfrom = "from invTypes"
        sqlwhere = "where marketGroupID={0}".format(group[0])
        sqlwhere = "{0} and published=1".format(sqlwhere)
        cursor.execute('{0} {1} {2}'.format(sqlselect, sqlfrom, sqlwhere))
        invtypes += cursor.fetchall()

    return invtypes

def dict_convert(invtypes):
    volumes = {}
    for ship, volume in invtypes:
        ship = ship.replace(' ', '')
        ship = ship.replace('-', '')
        ship = ship.lower()
        volumes[ship] = volume

    return volumes

groups = get_child_groups(parent)
invtypes = get_invtypes(groups)

cursor.close()
connection.close()

volumes = dict_convert(invtypes)
print(json.dumps(volumes, indent=4, sort_keys=True, separators=(',',':')))
