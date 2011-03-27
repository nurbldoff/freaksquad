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
                self.data[z].append([0,]*self.xsize)

    def put_random_block(self, value):
        self.data [randint(0, self.zsize-1)] [randint(0, self.ysize-1)] [randint(0, self.xsize-1)] = value

    def put_block(self, pos, kind):
        self.data[pos.z][pos.y][pos.x] = kind

    def get_block(self, pos):
        return self.data[pos.z][pos.y][pos.x]
