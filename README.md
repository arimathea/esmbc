ESMBC
=====

EVE Ship Maintenance Bay Calculator

Esmbc is a command line volume calculator written in Python. It would probably
be of most use to EVE pilots that own and fly Carriers.

Installation
------------

[Download a zip](https://github.com/stuartdb/esmbc/archive/master.zip) of this
repo or clone it:

```git clone git@github.com:stuartdb/seclit.git```

The only files you actually require are the main scrtip ```esmbc.py``` and the
date file of the ship volumes ```esmbc_data.json```

The only requirement for the is Python 3.


General Usage
-------------

Usage is fairly simple, esmbc takes ship:count pairs as arguments, that's it.

```python esmbc.py hound:3 talwar:2 sabre:1 rupture:1 hurricane:1 tornado:1```

The colon ```:``` character is used as the seperater and a space is used to
seperate ship:count pairs. Ship names can not contain spaces, if the ship name
normally contains a space, just remove it. So ```Republic Fleet Firetail```
would become ```republicfleetfiretail```.


Data File Generation
--------------------

If you are an end user and just wish to use escmb you can ignore this section.
The data file is included in the repository. For devs or curious power users the
```esmbcgenerate.py``` script is what is used to generate the json data file.

It uses the CCP community data dump and ```pymysql``` to generate the data.

Contact
--------------------

_Xikuan_ is the character to contact in game about esmbc, although creating
tickets here on github would be better.

License
--------------------

Seclit is released under the
[GPLv3 license](https://www.gnu.org/licenses/gpl.html)
