
A python package to handle projecting and unprojecting
a quadrilateralised spherical cube (quadsphere) lattice
of arbitrary size on a `⊢` ASCII net.

[![Travis Status](https://img.shields.io/travis/Goutte/quadsphere_lattice.svg)](https://travis-ci.org/Goutte/quadsphere_lattice)

Features
--------

- [x] Project to an ASCII net
- [x] Support Unicode
- [ ] Un-project from an ASCII net
- [ ] Find adjacent tiles
- [ ] Find neighbor tiles


Dependencies
------------

This library has no special dependencies,
and should work with both python 2.7 (and above), and 3.4 (and above).

You will need the python package `unittest` to run the test suite.


Testing
-------

```
$ python test_quadsphere_lattice.py
```

Alternatively, you can use `nose`, it will find and run the test file :

```
$ nosetests
```


Coordinates System
------------------

We're using integer coordinates in a cartesian system, on the face of the cube.

( 0, 0, 0 ) is the center of the cube. It's not a tile.
On the center of each face the coordinates would be :

```
  +-------+
  |       |
  | 0 1 0 |
  |       |
  +-------+-------+-------+-------+
  |       |       |       |       |
  | 0 0 -1| 1 0 0 | 0 0 1 |-1 0 0 |
  |       |       |       |       |
  +-------+-------+-------+-------+
  |       |
  | 0 -1 0|
  |       |
  +-------+
```

oriented as such (for when there are subdivisions) :

```
  +-------+
  |   △   |
  | x + ▷ |
  |   z   |
  +-------+-------+-------+-------+
  |   △   |   △   |   △   |   △   |
  | x + ▷ | z + ▷ | ◁ + x | ◁ + z |
  |   y   |   y   |   y   |   y   |
  +-------+-------+-------+-------+
  |   z   |
  | x + ▷ |
  |   ▽   |
  +-------+
```

Note that if were to print this net and make a cube, its markings would on the
interior of the cube, as the referential is right-handed.