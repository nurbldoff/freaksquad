from random import randint

class Level(object):
    def __init__(self, size=(10,10,3)):
        self.xsize, self.ysize, self.zsize = size
        self.empty()

    def empty(self):
        """
        Empty the level completely
        """
        self.data = []
        for z in range(self.zsize):
            self.data.append([])
            for y in range(self.ysize):
                self.data[z].append([])
                for x in range(self.xsize):
                    self.data[z][y].append(Block())

    def put_random_block(self, block):
        self.data [randint(0, self.zsize-1)] [randint(0, self.ysize-1)] [randint(0, self.xsize-1)] = block

    def put_block(self, pos, block):
        self.data[pos.z][pos.y][pos.x] = block

    def get_block(self, pos):
        return self.data[pos.z][pos.y][pos.x]


class Block(object):
    """
    This is the basic building block of the world.

    walls : a dict.
    """

    def __init__(self, walls=None, floor=None):
        if walls is None:
            self.walls = dict()
        else:
            self.walls = walls  # walls are numbered in positive direction starting from top
        self.floor = floor

    def get_wall(self, direction):
        if self.walls.has_key(direction):
            return self.walls[direction]
        else:
            return None

    def set_wall(self, direction, kind=1):
        self.walls[direction] = kind
