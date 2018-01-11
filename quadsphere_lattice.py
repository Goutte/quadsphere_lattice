def _norm(numeral_thingy):
    return 1 if numeral_thingy > 0 else -1 if numeral_thingy < 0 else 0


class Lattice:
    def __init__(self, size=1):
        """
        :param size: The side size (in tiles) of each face of the quadsphere.
                     This is NOT the binning depth as wikipedia defines.
                     Will yield a total of 6*size^2 tiles.
        """
        self.size = int(size)
        assert self.size > 0  # must be an unsigned int, or it makes no sense

        self.index = {}  # 'x,y,z' => tile value, usually a single character

    def __str__(self):
        return self.to_ascii_net()

    def to_ascii_net(self):
        """
        Dump the lattice as an ASCII net of a rubik's cube.
        Each tile will be cast to a single character.
        See the tests for how it looks.
        :return: string
        """
        h = '-'  # horizontal line
        v = '|'  # vertical line
        f = ' '  # default filler for empty tiles

        w = self.size
        s = ""

        def _vertical_separators_line(how_many, new_line=True):
            _s = "  %s" % v
            for j in range(how_many):
                _s += "   %s" % v
            if new_line:
                _s += "\n"
            return _s

        # Top face : 0 1 0
        for z in self._get_coords_range(invert=True):
            s += _vertical_separators_line(self.size - 1)

            s += "%s%s" % (h, h)
            for tile in self._get_tiles(y=w, z=z, default=f):
                s += "%.1s%s%s%s" % (tile, h, h, h)
            s = s[0:-1]  # remove extra horizontal line at the very end
            s += "\n"

        # Middle faces : 0 0 -1 | 1 0 0 | 0 0 1 | -1 0 0
        for y in self._get_coords_range(invert=True):
            s += _vertical_separators_line(self.size * 4 - 1)

            s += "%s%s" % (h, h)
            for tile in self._get_tiles(y=y, z=-w, default=f):
                s += "%.1s%s%s%s" % (tile, h, h, h)
            for tile in self._get_tiles(x=w, y=y, default=f):
                s += "%.1s%s%s%s" % (tile, h, h, h)
            for tile in self._get_tiles(y=y, z=w, default=f, invert=True):
                s += "%.1s%s%s%s" % (tile, h, h, h)
            for tile in self._get_tiles(x=-w, y=y, default=f, invert=True):
                s += "%.1s%s%s%s" % (tile, h, h, h)
            s = s[0:-1]  # remove extra horizontal line at the very end
            s += "\n"
        s += _vertical_separators_line(self.size * 4 - 1)

        # Bottom face : 0 -1 0
        for z in self._get_coords_range():
            s += "%s%s" % (h, h)
            for tile in self._get_tiles(y=-w, z=z, default=f):
                s += "%.1s%s%s%s" % (tile, h, h, h)
            s = s[0:-1]  # remove extra horizontal line at the very end
            s += "\n"

            s += _vertical_separators_line(self.size - 1)
        s = s[0:-1]  # remove the trailing carriage return

        return s

    def get_tile(self, x, y, z, default=None):
        k = "%d,%d,%d" % (x, y, z)
        if k in self.index:
            return self.index[k]
        else:
            return default

    def set_tile(self, x, y, z, value):
        k = "%d,%d,%d" % (x, y, z)
        self.index[k] = value

    def is_valid_coordinates(self, x, y, z):
        r = self._get_coords_range()
        return \
            (abs(x) == self.size and y in r and z in r) or \
            (abs(y) == self.size and z in r and x in r) or \
            (abs(z) == self.size and x in r and y in r)

    def get_adjacent_coordinates(self, xyz):
        adjacent = []

        x = xyz[0]
        y = xyz[1]
        z = xyz[2]

        face = self._get_offset_of_cube_face_axis(xyz=xyz)

        if face == 0:
            adjacent.append(self.normalize([x + 0, y + 2, z + 0]))
            adjacent.append(self.normalize([x + 0, y - 2, z + 0]))
            adjacent.append(self.normalize([x + 0, y + 0, z + 2]))
            adjacent.append(self.normalize([x + 0, y + 0, z - 2]))
        elif face == 1:
            adjacent.append(self.normalize([x + 2, y + 0, z + 0]))
            adjacent.append(self.normalize([x - 2, y + 0, z + 0]))
            adjacent.append(self.normalize([x + 0, y + 0, z + 2]))
            adjacent.append(self.normalize([x + 0, y + 0, z - 2]))
        elif face == 2:
            adjacent.append(self.normalize([x + 2, y + 0, z + 0]))
            adjacent.append(self.normalize([x - 2, y + 0, z + 0]))
            adjacent.append(self.normalize([x + 0, y + 2, z + 0]))
            adjacent.append(self.normalize([x + 0, y - 2, z + 0]))

        # print([a for a in adjacent if self.is_valid_coordinates(*a)])
        # return [a for a in adjacent if self.is_valid_coordinates(*a)]

        return adjacent

    def _get_offset_of_cube_face_axis(self, xyz):
        for i in range(3):
            if abs(xyz[i]) == self.size:
                return i
        raise Exception("Coordinates %s have no cube face." % (xyz,))

    def _get_offset_of_overflowed_axis(self, xyz):
        for i in range(3):
            if abs(xyz[i]) > self.size:
                return i
        return -1

    def normalize(self, xyz):
        over = self._get_offset_of_overflowed_axis(xyz=xyz)
        while over > -1:
            face = self._get_offset_of_cube_face_axis(xyz=xyz)

            o = xyz[over]
            f = xyz[face]

            xyz[over] = min(self.size, max(-self.size, o))
            xyz[face] = f - _norm(f) * abs(o - _norm(o) * self.size)
            over = self._get_offset_of_overflowed_axis(xyz=xyz)

        return xyz

    @classmethod
    def from_ascii_net(cls, net):
        # todo: refactor h and v
        h = '-'  # horizontal line
        v = '|'  # vertical line

        def convert(_char):  # dummy to allow override, which is todo
            return _char

        all_lines = net.split("\n")
        size = all_lines[0].count(v)

        lattice = cls(size=size)

        lines = []
        for i in range(1, len(all_lines), 2):
            lines.append(all_lines[i][2:-2].split("%s%s%s" % (h, h, h)))

        # Top face : 0 1 0
        y = size
        for z in lattice._get_coords_range(invert=True):
            line = lines.pop(0)
            for x in lattice._get_coords_range():
                v = convert(line.pop(0))
                lattice.set_tile(x=x, y=y, z=z, value=v)

        # Middle faces : 0 0 -1 | 1 0 0 | 0 0 1 | -1 0 0
        for y in lattice._get_coords_range(invert=True):
            line = lines.pop(0)
            z = -size
            for x in lattice._get_coords_range():
                v = convert(line.pop(0))
                lattice.set_tile(x=x, y=y, z=z, value=v)
            x = size
            for z in lattice._get_coords_range():
                v = convert(line.pop(0))
                lattice.set_tile(x=x, y=y, z=z, value=v)
            z = size
            for x in lattice._get_coords_range(invert=True):
                v = convert(line.pop(0))
                lattice.set_tile(x=x, y=y, z=z, value=v)
            x = -size
            for z in lattice._get_coords_range(invert=True):
                v = convert(line.pop(0))
                lattice.set_tile(x=x, y=y, z=z, value=v)

        # Bottom face : 0 -1 0
        y = -size
        for z in lattice._get_coords_range():
            line = lines.pop(0)
            for x in lattice._get_coords_range():
                v = convert(line.pop(0))
                lattice.set_tile(x=x, y=y, z=z, value=v)

        return lattice

    # PRIVATE #################################################################

    def _get_coords_range(self, invert=False):
        e = self.size - 1
        if invert:
            return [c for c in range(e, -1 * e - 1, -2)]
            # return range(e, -1 * e - 1, -2) todo benchmarking across git branches, maybe https://github.com/vstinner/perf
        else:
            return [c for c in range(-1 * e, 1 + e, 2)]

    def _get_tiles(self, x=None, y=None, z=None, invert=False, default=None):
        # type: (object, object, object, bool, object) -> list
        possible_coordinates = self._get_coords_range(invert=invert)
        if x is None:
            x = possible_coordinates
        elif not isinstance(x, list):
            x = [x]
        if y is None:
            y = possible_coordinates
        elif not isinstance(y, list):
            y = [y]
        if z is None:
            z = possible_coordinates
        elif not isinstance(z, list):
            z = [z]

        tiles = []
        for zz in z:
            for yy in y:
                for xx in x:
                    tiles.append(self.get_tile(xx, yy, zz, default=default))

        return tiles
