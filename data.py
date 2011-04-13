from random import randint
import os
import pygame
from utils import blit_mask, clip_masks

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
        if 0 <= pos.x < self.xsize and 0 <= pos.y < self.ysize and 0 <= pos.z < self.zsize:
            return self.data[pos.z][pos.y][pos.x]
        else:
            return None


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

    def set_wall(self, direction, kind=1, corners=True):
        self.walls[direction] = kind
        if corners and direction%2 == 1:
            self.walls[(direction+1)%8] = self.walls[(direction-1)%8] = kind

    def remove_wall(self, direction, corners=True):
        if self.walls.has_key(direction):
            del self.walls[direction]
        if corners and direction%2 == 1:
            if self.walls.has_key((direction+1)%8):
                del self.walls[(direction+1)%8]
            if self.walls.has_key((direction-1)%8):
                del self.walls[(direction-1)%8]


class Texture(object):
    """
    A container for a texture. Needs three faces (left, right and top) and a
    unique name for identification
    """

    def __init__(self, filenames, name):
        self.name = name
        self.load_image(filenames, name)
        self.cache = {}
        #self.thinwalls = [pygame.image.load("gfx/thinwall%d.png"%i).convert() for i in range(8)]
        self.topmask = pygame.image.load("gfx/block_top_white.png").convert_alpha()
        #for i in range(len(self.thinwalls)):
        #    self.get_texture("concrete").make_wall(self.thinwalls[i], i, 1)

    def load_image(self, imgfile, name):
        img = pygame.image.load(imgfile).convert_alpha()
        imgwidth = img.get_width()/3
        self.images = [img.subsurface(pygame.Rect(i*imgwidth,0,imgwidth,img.get_height()))
                                      for i in range(3)]

    def make_wall(self, direction, thickness):
        """
        Cuts the appropriate parts from a cube texture to build a wall section.
        """
        if (direction, thickness) in self.cache:
            return self.cache[(direction, thickness)]
        print "making texture"
        surf = self.topmask.copy()   #self.thinwalls[direction].copy()
        surf.fill((0,0,0,0))
        #pygame.Surface(self.images[0].get_size(), pygame.SRCALPHA)

        leftwall, rightwall, top = self.images
        srect = surf.get_rect()
        if direction == 0:
            trect = leftwall.get_rect()
            trect.width = thickness*2
            surf.blit(leftwall, (srect.width/2-thickness*2, -srect.width/4+thickness), trect)
            trect.left = srect.width - thickness*2
            surf.blit(rightwall, (srect.width/2, -srect.width/4+thickness), trect)
            topmask, toprect = clip_masks((self.topmask, self.topmask),
                                ((0,0),(0, -srect.width/2+2*thickness)))
            blit_mask(top, surf, toprect.topleft, topmask, toprect)

        if direction == 1:
            trect = leftwall.get_rect()
            trect.width = srect.width/2 - 2*thickness*2
            trect.left = srect.width/2+thickness*2
            surf.blit(rightwall, (2*thickness*2, -srect.width/4+thickness),trect)
            trect.left = 0
            trect.width = thickness*2
            surf.blit(leftwall, (thickness*2, -thickness), trect)
            topmask, toprect = clip_masks((self.topmask, self.topmask, self.topmask),
                                ((-2*thickness, thickness),(2*thickness, -thickness),
                                 (-srect.width/2+2*thickness, -srect.width/4+thickness)))
            blit_mask(top, surf, toprect.topleft, topmask, toprect)
            print toprect

        if direction == 2:
            trect = leftwall.get_rect()
            trect.width = thickness*2
            surf.blit(leftwall, (0,0), trect)
            trect.left = srect.width/2
            surf.blit(rightwall, (thickness*2, -srect.width/4+thickness), trect)
            topmask, toprect = clip_masks((self.topmask, self.topmask),
                                ((0,0),(-srect.width+4*thickness, 0)))
            blit_mask(top, surf, toprect.topleft, topmask, toprect)

        if direction == 3:
            trect = leftwall.get_rect()
            trect.width = srect.width/2 - 2*thickness*2
            trect.left = thickness*2
            surf.blit(leftwall, (thickness*2, 0), trect)
            trect.left = srect.width/2
            trect.width = thickness*2
            surf.blit(rightwall, (srect.width/2-thickness*2, -thickness), trect)
            topmask, toprect = clip_masks((self.topmask, self.topmask, self.topmask),
                                ((2*thickness, thickness),(-2*thickness, -thickness),
                                 (-srect.width/2+2*thickness, srect.width/4-thickness)))
            blit_mask(top, surf, toprect.topleft, topmask, toprect)


        if direction == 4:
            trect = leftwall.get_rect()
            trect.width = thickness*2
            trect.left = srect.width/2 - 2*thickness
            surf.blit(leftwall, trect.topleft, trect)
            trect.left = srect.width/2
            surf.blit(rightwall, trect.topleft, trect)
            topmask, toprect = clip_masks((self.topmask, self.topmask),
                                ((0,0),(0, srect.width/2-2*thickness)))
            blit_mask(top, surf, toprect.topleft, topmask, toprect)

        if direction == 5:
            trect = leftwall.get_rect()
            trect.width = srect.width/2 - 2*thickness*2
            trect.left = srect.width/2+thickness*2
            surf.blit(rightwall, (srect.width/2+thickness*2, 0), trect)
            trect.left = srect.width/2-thickness*2
            trect.width = thickness*2
            surf.blit(leftwall, (srect.width/2, -thickness), trect)
            topmask, toprect = clip_masks((self.topmask, self.topmask, self.topmask),
                                ((-2*thickness, thickness),(2*thickness, -thickness),
                                 (srect.width/2-2*thickness, srect.width/4-thickness)))
            blit_mask(top, surf, toprect.topleft, topmask, toprect)


        if direction == 6:
            trect = leftwall.get_rect()
            trect.width = thickness*2
            trect.left = srect.width/2 - 2*thickness
            surf.blit(leftwall, (srect.width-2*2*thickness, -srect.width/4+thickness), trect)
            trect.left = srect.width - thickness*2
            surf.blit(rightwall, trect.topleft, trect)
            topmask, toprect = clip_masks((self.topmask, self.topmask),
                                ((0,0),(srect.width-4*thickness, 0)))
            blit_mask(top, surf, toprect.topleft, topmask, toprect)

        if direction == 7:
            trect = leftwall.get_rect()
            trect.width = srect.width/2 - 2*thickness*2
            trect.left = thickness*2
            surf.blit(leftwall, (srect.width/2, -srect.width/4+thickness), trect)
            trect.width = srect.width/2
            trect.left = srect.width-thickness*2
            surf.blit(rightwall, (srect.width-2*thickness*2, -thickness), trect)
            topmask, toprect = clip_masks((self.topmask, self.topmask, self.topmask),
                                ((2*thickness, thickness),(-2*thickness, -thickness),
                                 (srect.width/2-2*thickness, -srect.width/4+thickness)))
            blit_mask(top, surf, toprect.topleft, topmask, toprect)

        self.cache[(direction, thickness)] = surf
        return surf

class Graphics(object):
    """
    A container for images. Should be smarter.
    """
    def __init__(self):
        self.textures = []
        self.path = "gfx/textures"

        self.block_img = pygame.image.load("gfx/block_textured.png").convert_alpha()
        self.block_half_img = pygame.image.load("gfx/block_half.png").convert_alpha()
        self.floor_img = pygame.image.load("gfx/floor.png").convert_alpha()
        self.block_rect = self.block_img.get_rect()
        self.block_height = 36
        self.block_width = 64
        self.block_depth = 32

        # self.load_texture(("gfx/block_textured_leftwall.png",
        #                    "gfx/block_textured_rightwall.png",
        #                    "gfx/block_textured_top.png"), "concrete")
        # self.load_texture(("gfx/test_texture_left.png",
        #                    "gfx/test_texture_right.png",
        #                    "gfx/test_texture_top.png"), "test")
        self.load_all_textures()

        # UFO/XCOM graphics found on the internets. Included only as placeholders!
        self.run_anim = [pygame.transform.scale2x(pygame.image.load("gfx/xcom0pm_run%d.tga"%(i))) for i in (8,7,6,5,4,3,2,1)]
        self.stand_anim = [pygame.transform.scale2x(pygame.image.load("gfx/xcom0pm_stand%d.tga"%i)) for i in (8,7,6,5,4,3,2,1)]

        self.cursor_img = pygame.image.load("gfx/cursor.png")
        self.cursor_rect = self.block_img.get_rect()

    def load_texture(self, imgfile, name):
        self.textures.append(Texture(imgfile, name))

    def load_all_textures(self):
        fs = os.listdir(self.path)
        for f in filter(lambda x: x.endswith(".png"), fs):
            txname = f.split(".")[0]
            tx = self.get_texture(txname)
            if not tx is None:
                self.textures.remove(tx)
            self.load_texture(os.path.join(self.path, f), txname)

    def get_texture(self, name):
        # This should be something more efficient
        for t in self.textures:
            if t.name == name:
                return t
        return None

    def get_texture_names(self):
        return [texture.name for texture in self.textures]

    def get_frame(self, img, n, ntot):
        w, h = img.get_size()
        return img.subsurface( pygame.Rect(n*w/ntot, 0, w/ntot, h) )


class Entity(pygame.sprite.Sprite):
    def __init__(self, name, stand_imgs, walk_imgs, walk_frames=8, position=(0,0,0), direction=0):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.stand_imgs = stand_imgs
        self.walk_imgs = walk_imgs
        self.walk_frames = walk_frames

        self.position = position
        self.direction = direction

        # sprite stuff
        self.rect = pygame.Rect((0,0), self.stand_imgs[0].get_size())
        self.image = self.stand_imgs[direction]

    def get_walk_frame(self, direction, n):
        """
        """
        w, h = self.rect.size
        ntot = self.walk_frames
        return self.walk_imgs[direction].subsurface( pygame.Rect(n*w, 0, w, h) )

    def get_stand_image(self):
        """
        """
        return self.stand_imgs[self.direction]


