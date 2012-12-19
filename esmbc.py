#!/usr/bin/env python

import sys

smalimit = 1000000
smatotal = 0

ships = {
    'cheetah': 17400,
    'firetail': 16500,
    'hound': 28100,
    'loki': 80000,
    'panther': 414000,
    'prowler': 180000,
    'rapier': 85000,
    }

for arg in sys.argv:
    entry = arg.split(':')

    if len(entry) == 2:
        ship = entry[0]
        count = entry[1]
    else:
        print('bad argument')
        continue

    if ship in ships:
       print('adding {0} {1}s'.format(count, ship))
       smatotal += ships[ship] * int(count)

print('current sma: {0}/{1}m3'.format(smatotal, smalimit))
