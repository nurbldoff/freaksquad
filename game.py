from __future__ import division

from collections import namedtuple
import sys, pygame
from random import randint
import pickle

import data
from vector import Vector
from utils import constrain, rotate_xypos, darken

# colors
BLACK = 0,0,0

pygame.init()

class View(object):
    def __init__(self, size=(640,480), level=None, position=(0,0,0)):
        self.size = size #width, height
        self.level = level
        self.position = Vector(*position)
        self.rotation = 0

        self.screen = pygame.display.set_mode(size)
        self.offscreen_back = pygame.Surface(self.screen.get_size())
        self.offscreen_front = pygame.Surface(self.screen.get_size())
        self.clock = pygame.time.Clock()

        self.graphics = data.Graphics()
        self.textures = self.graphics.get_texture_names()
        self.texture = self.textures[0]

        self.font = pygame.font.Font(None, 25)

        self.character_pos = [(0,3,0), (5, 5, 0), (7,2,0)]

        self.soldiers = pygame.sprite.RenderUpdates()
        for i,p in enumerate(self.character_pos):
            self.soldiers.add(data.Entity("soldier%d"%i, self.graphics.stand_anim,
                                          self.graphics.run_anim, p, randint(0,7)))

    def move_cursor_on_screen(self, dx=0, dy=0, dz=0):
        if self.rotation == 1:
            dx, dy = -dy, dx
        if self.rotation == 2:
            dx, dy = -dx, -dy
        if self.rotation == 3:
            dx, dy = dy, -dx
        v.position.x = constrain(v.position.x+dx, 0, lv.xsize-1)
        v.position.y = constrain(v.position.y+dy, 0, lv.ysize-1)
        v.position.z = constrain(v.position.z+dz, 0, lv.zsize-1)
        return v.position

    def get_screen_center(self):
        return self.size[0]//2, self.size[1]//2

    def map2screen(self, x, y, z):
        "Convert from map position to screen coordinates"
        cx, cy = self.get_screen_center()
        rx, ry = rotate_xypos(x, y, self.level.xsize-1, self.level.ysize-1,
                                        (self.rotation)%4)
        posx, posy = rotate_xypos(self.position.x, self.position.y,
                                  self.level.xsize-1, self.level.ysize-1,
                                  (-self.rotation)%4)
        posz = self.position.z
        return (cx+self.graphics.block_width//2*(posx-posy-x+y),
                cy+self.graphics.block_depth//2*(-posx-posy+x+y)-self.graphics.block_height*(z-posz))

    def screen2map(self, x, y, z):
        "Convert from screen coordinates to map position, in the given z plane."
        cx, cy = self.get_screen_center()
        w, h, d = self.graphics.block_width, self.graphics.block_height, self.graphics.block_depth
        dx, dy = ((x-cx-w//2), (y-cy+(z-self.position.z)*h-d//2))
        if self.rotation%4 == 0:
            rx, ry = (self.position.x + -dx/w + dy/d, self.position.y + dy/d + dx/w + 1)
        elif self.rotation%4 == 1:
            rx, ry = ( self.position.x - ( dy/d + dx/w), self.position.y + -dx/w + dy/d)
        elif self.rotation%4 == 2:
            rx, ry = ( self.position.x -( -dx/w + dy/d)+1, self.position.y - (dy/d + dx/w))
        elif self.rotation%4 == 3:
            rx, ry = ( self.position.x + dy/d + dx/w +1, self.position.y  - ( -dx/w + dy/d)+1)

        if 0 <= rx < self.level.xsize and 0 <= ry < self.level.ysize:
            return (int(rx), int(ry))
        else:
            return None


    def blit_block(self, pos, rect):
        x, y, z = pos
        bl = self.level.get_block(Vector(x, y, z))
        surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        if bl is not None:
             darkness = 4*(9-x+9-y+9-z)
             if bl.floor == 0:
                 floor = darken(self.graphics.floor_img, darkness)
                 surf.blit(floor, (0,0))

             # draw walls from the back
             for w in [(r+self.rotation*2)%8 for r in (0,1,7)]:
                 if bl.walls.has_key(w):
                     wall = darken(self.graphics.get_texture(self.texture).make_wall((w-self.rotation*2)%8, 2), darkness)
                     surf.blit(wall, (0,0))

             # draw higher floor (if any)
             if bl.floor == 0.5:
                 floor = darken(self.graphics.block_half_img, darkness)
                 surf.blit(floor, (0,0))
             elif bl.floor == 1:
                 floor = darken(self.graphics.block_img, darkness)
                 surf.blit(floor, (0,0))

             # just add some fake dudes
             if (x, y, z) in self.character_pos:
                 char_img = self.graphics.stand_anim[(x+y+z+2*self.rotation)%8]
                 surf.blit(char_img, ((rect.width - char_img.get_width())/2,
                                      (rect.height - char_img.get_height())/2-10))

             # draw walls in front
             for w in [(r+self.rotation*2)%8 for r in (2,6,3,5,4)]:
                 if bl.walls.has_key(w):
                     wall = darken(self.graphics.get_texture(self.texture).make_wall((w-self.rotation*2)%8, 2),
                                   darkness)
                     surf.blit(wall, (0,0))
                     #surf.blit(self.graphics.thinwalls[(w-self.rotation*2)%8], (0,0))

             #if x+y > self.position.x+self.position.y:
             #    surf.set_alpha(127)
             return surf
        else:
            return None


    def draw(self):
        cx, cy = self.get_screen_center()
        self.screen.fill(BLACK)
        rect=self.graphics.block_rect
        self.offscreen_back.fill((0,0,0))

        for z in range(self.level.zsize):
            for a in range(self.level.xsize+self.level.ysize):
                if a >= self.level.xsize:
                    c = a - self.level.xsize   #self.level.ysize+self.level.xsize-1-a
                else:
                    c = 0
                for y in range(c,a-c):
                    x = a-y-1
                    rx, ry = rotate_xypos(x, y, self.level.xsize-1, self.level.ysize-1,
                                        (self.rotation)%4)
                    rect.center = self.map2screen(x,y,z)

                    # Check that we're not drawing outside the screen, which would be
                    # a waste of time.
                    if rect.clip(self.screen.get_rect()).size != (0,0):

                        surf = self.blit_block((rx, ry, z), rect)
                        if surf is not None:
                            self.offscreen_back.blit(surf, rect)
                        if (rx, ry, z) == (self.position.x, self.position.y, self.position.z):
                            print "drawing cursor"
                            self.offscreen_back.blit(self.graphics.cursor_img, rect)


        #print v.position

        self.screen.blit(self.offscreen_back, (0,0))

        postext = self.font.render("%d, %d, %d"%v.position.tuple(), 1, (255,255,0))
        self.screen.blit(postext, (10,10))

        pygame.display.update()



lv = data.Level(size=(10,10,10))

for i in range(10):
    lv.put_block(Vector(i,0,0), data.Block(walls={0:1}))
    lv.put_block(Vector(0,2,i), data.Block(walls={7:1}))
    lv.put_block(Vector(0,i,0), data.Block(walls={0:1, 1:1, 2:1, 3:1, 4:1, 5:1, 6:1, 7:1}))
    #lv.put_block(Vector(0,i,0), data.Block(walls={1:1, 3:1, 5:1, 7:1}, floor=0.5))


#for i in range(100):
#    d.set_random_block(1)

v = View(level=lv)
v.draw()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            p = v.screen2map(*event.pos, z=v.position.z)
            if p is not None:
                print "Mouse at:", p
            else:
                print "You moused outside!"

        elif event.type == pygame.KEYDOWN:
            print event.key
            bl = v.level.get_block(v.position)
            direction = -1

            if event.key == pygame.K_LEFT:
                v.move_cursor_on_screen(dx=1)
            elif event.key == pygame.K_RIGHT:
                v.move_cursor_on_screen(dx=-1)
            elif event.key == pygame.K_DOWN:
                v.move_cursor_on_screen(dy=1)
            elif event.key == pygame.K_UP:
                v.move_cursor_on_screen(dy=-1)
            elif event.key == pygame.K_PAGEUP:
                v.move_cursor_on_screen(dz=1)
            elif event.key == pygame.K_PAGEDOWN:
                v.move_cursor_on_screen(dz=-1)

            elif event.key == pygame.K_r:
                v.rotation = (v.rotation+1)%4
            elif event.key == pygame.K_t:
                v.rotation = (v.rotation-1)%4

            elif event.key == pygame.K_SPACE:
                if bl.floor == None:
                    bl.floor = 1
                elif bl.floor == 1:
                    bl.floor = 0.5
                elif bl.floor == 0.5:
                    bl.floor = 0
                elif bl.floor == 0:
                    bl.floor = None

            elif event.key == pygame.K_f:
                v.texture = v.textures[(v.textures.index(v.texture) + 1)%len(v.textures)]

            elif event.key == pygame.K_TAB:
                v.graphics.load_all_textures()
                v.textures = v.graphics.get_texture_names()

            if event.key == pygame.K_k:
                filename = raw_input("Filename to SAVE level: ")
                if filename != "":
                    try:
                        with open(filename, "w") as f:
                            pickle.dump(v.level, f)
                    except IOError:
                        print "Could not open file!"

            if event.key == pygame.K_l:
                filename = raw_input("Filename to LOAD level: ")
                if filename != "":
                    try:
                        with open(filename) as f:
                            v.level = pickle.load(f)
                    except IOError:
                        print "Could not open file!"



            elif event.key in (pygame.K_e, pygame.K_KP9):
                direction = 0
            elif event.key in (pygame.K_w, pygame.K_KP8):
                direction = 1
            elif event.key in (pygame.K_q, pygame.K_KP7):
                direction = 2
            elif event.key in (pygame.K_a, pygame.K_KP4):
                direction = 3
            elif event.key in (pygame.K_z, pygame.K_KP1):
                direction = 4
            elif event.key in (pygame.K_x, pygame.K_KP2):
                direction = 5
            elif event.key in (pygame.K_c, pygame.K_KP3):
                direction = 6
            elif event.key in (pygame.K_d, pygame.K_KP6):
                direction = 7

            if direction > -1:
                rotdir = (direction+v.rotation*2)%8
                if bl.get_wall(rotdir) is not None:
                    bl.remove_wall(rotdir)
                else:
                    bl.set_wall(rotdir, 1)

            v.draw()

    v.clock.tick(240)



"""
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        ballrect = ballrect.move(speed)
        if ballrect.left < 0 or ballrect.right > width:
            speed[0] = -speed[0]
        if ballrect.top < 0 or ballrect.bottom > height:
            speed[1] = -speed[1]

        screen.fill(black)
        screen.blit(ball, ballrect)
        pygame.display.flip()
"""
