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

    def __init__(self, tree=0, block_imgs=None, block_size=None):
        self.tree = tree
        if block_imgs is not None:
            self.block_imgs = block_imgs
            self.block_rects = [bl.get_rect() for bl in block_imgs]
        if block_size is not None:
            self.wx, self.hx, self.wy, self.hy, self.hz = block_size

        self.surface = pygame.Surface((self.block_rects[0].size), flags=pygame.SRCALPHA)
        self.tainted = True
        self.zoom = 1
        self.rotation = 0


    def get_rect(self):
        surfsize = self.surface.get_size()
        return pygame.Rect((0,0),(surfsize[0], surfsize[1]))

    def draw(self, zoom, rotation=0):
        #print zoom
        if self.tainted or zoom != self.zoom or rotation != self.rotation:
            if zoom != self.zoom:
                self.zoom = zoom
                self.surface = pygame.Surface((self.block_rects[0].width*zoom,
                                               self.block_rects[0].height*zoom), flags=pygame.SRCALPHA)
            if self.rotation != rotation:
                self.rotation = rotation
            self.surface.fill((0,0,0,0))
            draw_octree(self.surface, self.block_imgs, (self.wx, self.hx, self.wy, self.hy, self.hz),
                        self.tree, 0, zoom=zoom, rotation=rotation)
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
                    #if all(tree):

                    tree[n] = kind
                else:
                    if tree[n] == 0:
                        tree[n] = tmp = [0,0,0,0,0,0,0,0]
                        tree = tmp
                    elif tree[n] == 1:
                        return
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


def rotate_nodes(nodes, n):
    new = nodes[:]
    for i in range(n):
        new = [new[1], new[3], new[0], new[2], new[5], new[7], new[4], new[6]]
    return new

def draw_octree(surf, block_imgs, offsets, tree, level, maxlevel=4, zoom=1, rotation=0):
    print "draw_octree, rota =", rotation
    print "draw_octree, zoom =", zoom
    if zoom == 2:
        block_imgs = [pygame.transform.scale2x(block_imgs[0]),] + block_imgs
    if type(tree).__name__ == "int":
        if tree > 0:
            #print "draw", level, offsets
            surf.blit(block_imgs[level], (0,0))
    else:
        #f = 2**(level+1)
        wx, hx, wy, hy, hz = [zoom*o//2 for o in offsets]

        rect = surf.get_rect()
        rect.size = (rect.width//2, rect.height//2)
        #for i,tr in enumerate(tree[4-rotation:4]+tree[:4-rotation]+tree[8-rotation:]+tree[4:8-rotation]):
        #for i,tr in enumerate(tree[rotation:4]+tree[:rotation]+tree[4+rotation:]+tree[4:4+rotation]):
        for i, tr in enumerate(rotate_nodes(tree, rotation)):
            #rect = surf.get_rect()
            # a trick using binary representation to get position coordinates
            z, y, x = [int(x) for x in string.zfill(bin(i)[2:], 3)]
            # if rotation == 1:
            #     x, y = y, 1-x
            # elif rotation == 2:
            #     x, y = 1-x, 1-y
            # elif rotation == 3:
            #     x, y = 1-y, x
            ##print x, y, z
            rect.topleft = (x*wx+(1-y)*wy, y*hy+x*hx+(1-z)*hz)
            #rect.topleft = ((1-x)*wx+y*wy, y*hy+x*hx+(1-z)*hz)
            ##print rect.topleft
            s = surf.subsurface(rect)
            if level < maxlevel:
                draw_octree(s, block_imgs, (wx, hx, wy, hy, hz), tr, level+1, rotation=rotation)



