from __future__ import division

from collections import namedtuple
import sys, pygame
import data
from vector import Vector

# colors
BLACK = 0,0,0

def constrain(value, minlim, maxlim):
    "Return the value if it lies between max and min inclusive, otherwise return the closest of max ang min."
    return max(minlim, min(maxlim, value))


pygame.init()

class View(object):
    def __init__(self, size=(640,480), level=None, position=(0,0,0)):
        self.size = size #width, height
        self.level = level
        self.position = Vector(*position)

        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()

        self.block_img = pygame.image.load("block.png")
        self.block_rect = self.block_img.get_rect()
        self.block_height = 31
        self.block_width = 52
        self.block_depth = 26

        self.cursor_img = pygame.image.load("cursor.png")
        self.cursor_rect = self.block_img.get_rect()

        self.font = pygame.font.Font(None, 25)

    def draw(self):
        cx, cy = self.get_screen_center()
        posx, posy, posz = self.position.x, self.position.y, self.position.z
        self.screen.fill(BLACK)
        for z in range(self.level.zsize):
            for y in range(self.level.ysize):
                for x in range(self.level.xsize):
                    if self.level.data[z][y][x] == 1:
                        rect=self.block_rect
                        rect.center = (cx-self.block_width//2*(posx-posy-x+y),
                                       cy-self.block_depth//2*(posy+posx-x-y)-self.block_height*(z-posz))
                        self.screen.blit(self.block_img, rect)
                    if (x, y, z) == (self.position.x, self.position.y, self.position.z):
                        print "drawing cursor"
                        rect.center = (cx-self.block_width//2*(posx-posy-x+y),
                                       cy-self.block_depth//2*(posy+posx-x-y)-self.block_height*(z-posz))
                        self.screen.blit(self.cursor_img, rect)
        #print v.position
        postext = self.font.render("%d, %d, %d"%v.position.tuple(), 1, (255,255,0))
        self.screen.blit(postext, (10,10))
        pygame.display.flip()

    def get_screen_center(self):
        return self.size[0]//2, self.size[1]//2

lv = data.Level(size=(10,10,10))

for i in range(10):
    lv.data[0][0][i] = 1
    lv.data[0][2][i] = 1
    lv.data[0][i][0] = 1
    lv.data[1][i][0] = 1

#for i in range(100):
#    d.set_random_block(1)

v = View(level=lv)
v.draw()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.KEYDOWN:
            print event.key

            if event.key == pygame.K_RIGHT:
                v.position.x = constrain(v.position.x+1, 0, lv.xsize-1)
            elif event.key == pygame.K_LEFT:
                v.position.x = constrain(v.position.x-1, 0, lv.xsize-1)
            elif event.key == pygame.K_DOWN:
                v.position.y = constrain(v.position.y+1, 0, lv.ysize-1)
            elif event.key == pygame.K_UP:
                v.position.y = constrain(v.position.y-1, 0, lv.ysize-1)
            elif event.key == pygame.K_PAGEUP:
                v.position.z = constrain(v.position.z+1, 0, lv.zsize-1)
            elif event.key == pygame.K_PAGEDOWN:
                v.position.z = constrain(v.position.z-1, 0, lv.zsize-1)

            elif event.key == pygame.K_SPACE:
                if lv.get_block(v.position) == 0:
                    lv.put_block(v.position, 1)
                else:
                    lv.put_block(v.position, 0)

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
