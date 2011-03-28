from __future__ import division

from random import randint
import string
import pygame

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

    def put_random_block(self, value):
        self.data [randint(0, self.zsize-1)] [randint(0, self.ysize-1)] [randint(0, self.xsize-1)] = value

    def put_block(self, pos, block):
        if type(pos).__name__ == "tuple":
            self.data[pos[2]][pos[1]][pos[0]] = block
        else:
            self.data[pos.z][pos.y][pos.x] = block

    def get_block(self, pos):
        if type(pos).__name__ == "tuple":
            return self.data[pos[2]][pos[1]][pos[0]]
        else:
            return self.data[pos.z][pos.y][pos.x]


class Block(object):
    """
    """

    block_imgs = [pygame.image.load("block2.png"),
                  pygame.image.load("block2b.png"),
                  pygame.image.load("block2c.png"),
                  pygame.image.load("block2d.png")]
    block_rects = [bl.get_rect() for bl in block_imgs]

    hz = 32
    wx = 16
    hx = 16
    wy = 32
    hy = 8

    def __init__(self, tree=0):
        self.tree = tree
        self.surface = pygame.Surface((self.block_rects[0].size), flags=pygame.SRCALPHA)
        self.tainted = True

    def draw(self):
        if self.tainted:
            self.surface.fill((0,0,0,0))
            draw_octree(self.surface, self.block_imgs, (self.wx, self.hx, self.wy, self.hy, self.hz),
                        self.tree, 0)
            self.tainted=False

    def put_sub_element(self, scale, position, kind):
        if scale == 0:
            self.tree = 1
            self.tainted = True
        else:
            if self.tree == 0:
                self.tree = [0,0,0,0,0,0,0,0]
            elif self.tree == 1:
                return   #nothing to be done!
            tree = self.tree
            x, y, z = position
            print "scale:", scale
            for i in range(scale,0,-1):
                # calculate block index from coordinates
                d = 2**(i-1)
                lx = x // d
                ly = y // d
                lz = z // d
                x -= lx*d
                y -= ly*d
                z -= lz*d
                n = lz*4+ly*2+lx
                #print "n=",n

                if i == 1:
                    tree[n] = kind
                else:
                    if tree[n] == 0:
                        tree[n] = tmp = [0,0,0,0,0,0,0,0]
                        tree = tmp
                    elif tree[n] == 1:
                        pass
                    else:
                        tree = tree[n]
            self.tainted=True

    def remove_sub_element(self, scale, position):
        if scale == 0:
            self.tree = 0
            self.tainted=True
        else:
            if self.tree == 1:
                self.tree = [1,1,1,1,1,1,1,1]
            elif self.tree == 0:
                return   #nothing needs to be done!
            tree = self.tree
            x, y, z = position
            print "scale:", scale
            for i in range(scale,0,-1):
                d = 2**(i-1)
                lx = x // d
                ly = y // d
                lz = z // d
                x -= lx*d
                y -= ly*d
                z -= lz*d
                n = lz*4+ly*2+lx
                print "n=",n

                if i == 1:
                    tree[n] = 0
                else:
                    if tree[n] == 1:
                        tree[n] = tmp = [1,1,1,1,1,1,1,1]
                        tree = tmp
                    elif tree[n] == 0:
                        exit
                    else:
                        tree = tree[n]
            self.tainted=True




def draw_octree(surf, block_imgs, offsets, tree, level, maxlevel=4):
    if type(tree).__name__ == "int":
        if tree > 0:
            #print "draw", level, offsets
            surf.blit(block_imgs[level], (0,0))
    else:
        #f = 2**(level+1)
        wx, hx, wy, hy, hz = [o//2 for o in offsets]

        rect = surf.get_rect()
        rect.size = (rect.width//2, rect.height//2)
        for i,tr in enumerate(tree):
            #rect = surf.get_rect()
            # a trick using binary representation to get position coordinates
            z, y, x = [int(x) for x in string.zfill(bin(i)[2:], 3)]
            ##print x, y, z
            rect.topleft = (x*wx+(1-y)*wy, y*hy+x*hx+(1-z)*hz)
            ##print rect.topleft
            s=surf.subsurface(rect)
            if level < maxlevel:
                draw_octree(s, block_imgs, (wx, hx, wy, hy, hz), tr, level+1)



