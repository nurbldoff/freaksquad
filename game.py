from __future__ import division

from collections import namedtuple
import sys, pygame
import data
from vector import Vector
from utils import constrain, texture_wall, rotate_xypos

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
        self.clock = pygame.time.Clock()

        self.graphics = data.Graphics()

        self.font = pygame.font.Font(None, 25)

        self.character_pos = [(0,3,0), (5, 5, 0), (7,2,0)]


    def get_cursor_position_on_screen(self):
        cp = self.position
        if self.rotation == 0:
            return cp
        elif self.rotation == 1:
            return Vector(cp.y, self.level.xsize-cp.x-1, cp.z)
        elif self.rotation == 2:
            return Vector(self.level.xsize-cp.x-1, self.level.ysize-cp.y-1, cp.z)
        elif self.rotation == 3:
            return Vector(self.level.ysize-cp.y-1, cp.x, cp.z)

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

    def draw(self):
        cx, cy = self.get_screen_center()
        self.screen.fill(BLACK)
        rect=self.graphics.block_rect
        for z in range(self.level.zsize):
            for y in range(self.level.ysize):
                for x in range(self.level.xsize):

                    rx, ry = rotate_xypos(x, y, self.level.xsize-1, self.level.ysize-1,
                                        (self.rotation)%4)
                    bl = self.level.get_block(Vector(rx, ry, z))
                    posx, posy = rotate_xypos(self.position.x, self.position.y,
                                              self.level.xsize-1, self.level.ysize-1,
                                              (-self.rotation)%4)
                    posz = self.position.z
                    #posx, posy, posz = self.get_cursor_position_on_screen().tuple()

                    # an offscreen bitmap to draw the block into
                    surf = pygame.Surface(rect.size, pygame.SRCALPHA)

                    rect.center = (cx+self.graphics.block_width//2*(+posx-posy-x+y),
                                   cy+self.graphics.block_depth//2*(-posx-posy+x+y)-\
                                       self.graphics.block_height*(z-posz))
                    # Check that we're not drawing outside the screen, which would be
                    # a waste of time.
                    if rect.clip(self.screen.get_rect()).size != (0,0):

                        if bl.floor == 0:
                            surf.blit(self.graphics.floor_img, (0,0))

                        # draw walls from the back
                        for w in [(r+self.rotation*2)%8 for r in (0,1,7)]:
                            if bl.walls.has_key(w):
                                surf.blit(self.graphics.thinwalls[(w-self.rotation*2)%8], (0,0))

                        # draw higher floor (if any)
                        if bl.floor == 0.5:
                            surf.blit(self.graphics.block_half_img, (0,0))
                        elif bl.floor == 1:
                            surf.blit(self.graphics.block_img, (0,0))

                        if (x, y, z) in self.character_pos:
                            char_img = self.graphics.stand_anim[3]
                            surf.blit(char_img, ((rect.width - char_img.get_width())/2,
                                                 (rect.height - char_img.get_height())/2-10))

                        # draw walls in front
                        for w in [(r+self.rotation*2)%8 for r in (2,6,3,5,4)]:
                            if bl.walls.has_key(w):
                                surf.blit(self.graphics.thinwalls[(w-self.rotation*2)%8], (0,0))

                        #if x+y > self.position.x+self.position.y:
                        #    surf.set_alpha(127)
                        self.screen.blit(surf, rect)

                        if (rx, ry, z) == (self.position.x, self.position.y, self.position.z):
                            print "drawing cursor"
                            #rect.center = (cx-self.block_width//2*(posx-posy-x+y),
                            #               cy-self.block_depth//2*(posy+posx-x-y)-self.block_height*(z-posz))

                            self.screen.blit(self.graphics.cursor_img, rect)

        #print v.position
        postext = self.font.render("%d, %d, %d"%v.position.tuple(), 1, (255,255,0))
        self.screen.blit(postext, (10,10))
        pygame.display.flip()

    def get_screen_center(self):
        return self.size[0]//2, self.size[1]//2



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
        elif event.type == pygame.KEYDOWN:
            print event.key
            bl = lv.get_block(v.position)
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
