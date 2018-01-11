#!/usr/bin/env python
# coding=utf-8

import unittest

from quadsphere_lattice import Lattice


class TestQuadsphereLattice(unittest.TestCase):

    def assertMultilineEquals(self, expected, actual):
        """
        Same as `assertEquals`, but has a multi line error message on failure,
        because it is more convenient and explicit in our case.
        """
        s = "Expected the net\n%s\nto be equal to\n%s" % (actual, expected)
        if expected != actual:
            self.fail(s)

    # ACTUAL TESTS ############################################################

    def test_initialization_empty(self):
        Lattice()

    def test_to_ascii_net_size_1(self):
        actual = Lattice(size=1).to_ascii_net()
        expected = """
  |
-- --
  |   |   |   |
-- --- --- --- --
  |   |   |   |
-- --
  |
""".strip("\n")  # we added line returns above to keep the net's readability
        self.assertMultilineEquals(expected, actual)

    def test_to_ascii_net_size_2(self):
        actual = Lattice(size=2).to_ascii_net()
        expected = """
  |   |
-- --- --
  |   |
-- --- --
  |   |   |   |   |   |   |   |
-- --- --- --- --- --- --- --- --
  |   |   |   |   |   |   |   |
-- --- --- --- --- --- --- --- --
  |   |   |   |   |   |   |   |
-- --- --
  |   |
-- --- --
  |   |
""".strip("\n")
        self.assertMultilineEquals(expected, actual)

    def test_to_ascii_net_with_tiles(self):
        lattice = Lattice(size=3)
        lattice.set_tile(3, 0, 0, 'X')
        lattice.set_tile(0, 3, 0, 'O')
        lattice.set_tile(2, -3, -2, '9')
        # overwriting should be allowed
        lattice.set_tile(0, 3, 2, 'E')
        lattice.set_tile(0, 3, 2, '&')
        # - character should be allowed
        lattice.set_tile(0, 0, 3, '-')
        # | character should be allowed
        lattice.set_tile(2, 0, 3, '|')
        # projection should truncate to one character per tile
        lattice.set_tile(0, 2, 3, '@@@')
        actual = lattice.to_ascii_net()
        expected = """
  |   |   |
-- ---&--- --
  |   |   |
-- ---O--- --
  |   |   |
-- --- --- --
  |   |   |   |   |   |   |   |   |   |   |   |
-- --- --- --- --- --- --- ---@--- --- --- --- --
  |   |   |   |   |   |   |   |   |   |   |   |
-- --- --- --- ---X--- ---|------- --- --- --- --
  |   |   |   |   |   |   |   |   |   |   |   |
-- --- --- --- --- --- --- --- --- --- --- --- --
  |   |   |   |   |   |   |   |   |   |   |   |
-- --- ---9--
  |   |   |
-- --- --- --
  |   |   |
-- --- --- --
  |   |   |
""".strip("\n")
        self.assertMultilineEquals(expected, actual)

    def test_to_ascii_net_with_unicode_tiles(self):
        lattice = Lattice(size=1)
        lattice.set_tile(1, 0, 0, u'✗')
        lattice.set_tile(0, 1, 0, u'❥')
        # projection should truncate to one unicode character per tile
        lattice.set_tile(0, 0, 1, u'✊✋✌')
        actual = lattice.to_ascii_net()
        expected = u"""
  |
--❥--
  |   |   |   |
-- ---✗---✊--- --
  |   |   |   |
-- --
  |
""".strip("\n")
        self.assertMultilineEquals(expected, actual)

    def test_from_ascii_net_size_2(self):
        net = """
  |   |
--X---X--
  |   |
-- --- --
  |   |   |   |   |   |   |   |
-- --- --- --- --- ---X---O--- --
  |   |   |   |   |   |   |   |
-- ---X--- ---O--- --- ---O--- --
  |   |   |   |   |   |   |   |
-- --- --
  |   |
-- ---X--
  |   |
""".strip("\n")
        lattice = Lattice.from_ascii_net(net)
        expected = net
        actual = lattice.to_ascii_net()

        self.assertMultilineEquals(expected, actual)

    def test_get_adjacent_coordinates(self):
        net = """
  |   |   |
-- --- --- --
  |   |   |
-- --- --- --
  |   |   |
--0--- --- --
  |   |   |   |   |   |   |   |   |   |   |   |
--1---0--- --- --- --- --- ---+--- --- --- ---0--
  |   |   |   |   |   |   |   |   |   |   |   |
--0--- --- --- ---X--- ---+---+---+--- --- --- --
  |   |   |   |   |   |   |   |   |   |   |   |
-- --- --- ---X---Z---X--- ---+--- --- --- --- --
  |   |   |   |   |   |   |   |   |   |   |   |
-- --- --- --
  |   |   |
-- --- ---X--
  |   |   |
-- --- --- --
  |   |   |
""".strip("\n")
        lattice = Lattice(size=3)

        tiles = [
            # (where, char on tile, char on adjacents)
            ((3, -2, 0), 'Z', 'X'),
            ((-2, 2, -3), '1', '0'),
            ((0, 0, 3), '+', '+'),
        ]

        for tile in tiles:
            lattice.set_tile(tile[0][0], tile[0][1], tile[0][2], tile[1])
            for adj in lattice.get_adjacent_coordinates(tile[0]):
                lattice.set_tile(adj[0], adj[1], adj[2], tile[2])

        expected = net
        actual = lattice.to_ascii_net()

        self.assertMultilineEquals(expected, actual)


if __name__ == '__main__':
    unittest.main()
