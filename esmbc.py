#!/usr/bin/env python

import sys
import json
import os

def load_ship_dict(filename):
    if os.path.exists(filename):
        with open(filename, 'rt') as esmbc_data:
            return json.load(esmbc_data)
    else:
        print('Unable to load ship and volume data file')
        sys.exit()

if __name__ == "__main__":
    print('{0}'.format(load_ship_dict('esmbc_data.json')))

    # smalimit = 1000000
    # smatotal = 0

    # del sys.argv[0]

    # for arg in sys.argv:
    # entry = arg.split(':')

    # if len(entry) == 2:
    #     ship = entry[0]
    #     count = entry[1]
    # else:
    #     print('bad argument')
    #     continue

    # if ship in ships:
    #    print('adding {0} {1}s'.format(count, ship))
    #    smatotal += ships[ship] * int(count)

    # print('current sma: {0}/{1}m3'.format(smatotal, smalimit))
