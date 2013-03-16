=====
ESMBC
=====

EVE Ship Maintenance Bay Calculator

Esmbc is a command line ship volume calculator for EVE online. It would probably
be of most use to EVE pilots that own and fly Carriers.

Usage
----------

``$ python esmbc.py hound:3 talwar:2 sabre:1 rupture:1 hurricane:1 tornado:1``

::
     43000m3 (sabre)
     86000m3 (talwar)
    216000m3 (tornado)
     96000m3 (rupture)
     84300m3 (hound)
    216000m3 (hurricane)
    741300m3

* Esmbc accepts ship names and quantities with the colon character as a seperator.
* The pairs are seperated by a single whitespace.
* Ship names which contain a white space or special character should have it removed.

``Republic Fleet Firetail`` should be entered as ``republicfleetfiretail``.

Installation
------------

`Download a zip <https://github.com/stuartdb/esmbc/archive/master.zip>`_ of this
repo or clone it.

``git clone git@github.com:stuartdb/seclit.git``

Requirements
------------

Esmbc was written against Python 3.3 as is the only requirement.

Ship/Volume Data File
---------------------

The ship and volume data file that is required is supplied (``data/ships.json``).

You also have the option to build your own data file. This may be required in
the future as CCP release new ship types.

A script is included to access a MYSQL version of the CCP community data dump.

``$ python esmbc_mysql.py > data/ships.json``

The ``pymysql`` module is a requirement of the data generation script.

License
--------------------

esmbc is released under the
`GPLv3 license <https://www.gnu.org/licenses/gpl.html>`_
