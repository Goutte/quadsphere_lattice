#!/usr/bin/env python

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


if __name__ == '__main__':
    unittest.main()
