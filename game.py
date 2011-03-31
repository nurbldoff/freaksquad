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

def get_wall_offset(n):
    if n == 0:
        return (0,-0.5)
    if n == 1:
        return (-0.25, -0.25)
    if n == 2:
        return (-0.5, 0)
    if n == 3:
        return (-0.25, 0.25)
    if n == 4:
        return (0, 0.5)
    if n == 5:
        return (0.25, 0.25)
    if n == 6:
        return (0.5, 0)
    if n == 7:
        return (0.25, -0.25)

pygame.init()

class View(object):
    def __init__(self, size=(640,480), level=None, position=(0,0,0)):
        self.size = size #width, height
        self.level = level
        self.position = Vector(*position)

        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()

        self.block_img = pygame.image.load("block.png")
        self.block_half_img = pygame.image.load("block_half.png")
        self.block_rect = self.block_img.get_rect()
        self.block_height = 32
        self.block_width = 56
        self.block_depth = 28

        self.wall1_img = pygame.image.load("wall1.png")
        self.wall2_img = pygame.image.load("wall2.png")
        self.corner_img = pygame.image.load("corner.png")

        self.thinwalls = [
            pygame.image.load("thinwall0.png"),
            pygame.image.load("thinwall1.png"),
            pygame.image.load("thinwall2.png"),
            pygame.image.load("thinwall3.png"),
            pygame.image.load("thinwall4.png"),
            pygame.image.load("thinwall5.png"),
            pygame.image.load("thinwall6.png"),
            pygame.image.load("thinwall7.png")
            ]

        self.cursor_img = pygame.image.load("cursor.png")
        self.cursor_rect = self.block_img.get_rect()

        self.font = pygame.font.Font(None, 25)

    def draw(self):
        cx, cy = self.get_screen_center()
        posx, posy, posz = self.position.x, self.position.y, self.position.z
        self.screen.fill(BLACK)
        rect=self.block_rect
        for z in range(self.level.zsize):
            for y in range(self.level.ysize):
                for x in range(self.level.xsize):
                    bl = self.level.get_block(Vector(x, y, z))

                    rect.center = (cx-self.block_width//2*(posx-posy-x+y),
                                   cy-self.block_depth//2*(posy+posx-x-y)-self.block_height*(z-posz))
                    # Check that we're not drawing outside the screen, which would be
                    # a waste of time.
                    if rect.clip(self.screen.get_rect()).size != (0,0):

                        for w in (0,1,7,2):  # draw walls from the back
                            if bl.walls.has_key(w):
                                #xfact, yfact = get_wall_offset(w)
                                #xoffs = xfact*rect.width
                                #yoffs = yfact*self.block_depth
                                #rect.center = (cx-self.block_width//2*(posx-posy-x+y)+xoffs,
                                #               cy-self.block_depth//2*(posy+posx-x-y)-self.block_height*(z-posz)+yoffs)

                                self.screen.blit(self.thinwalls[w], rect)
                                #self.screen.blit(self.thinwall7_img, rect)

                        # draw floor (if any)
                        if bl.floor is None:
                            pass
                        elif bl.floor <= 0.5:
                            rect.center = (cx-self.block_width//2*(posx-posy-x+y),
                                           cy-self.block_depth//2*(posy+posx-x-y)-self.block_height*(z-posz))
                            self.screen.blit(self.block_half_img, rect)
                        else:
                            rect.center = (cx-self.block_width//2*(posx-posy-x+y),
                                           cy-self.block_depth//2*(posy+posx-x-y)-self.block_height*(z-posz))
                            self.screen.blit(self.block_img, rect)

                        for w in (6,3,5,4):  # draw walls in front
                            if bl.walls.has_key(w):
                                #xfact, yfact = get_wall_offset(w)
                                #xoffs = xfact*rect.width
                                #yoffs = yfact*self.block_depth
                                #rect.center = (cx-self.block_width//2*(posx-posy-x+y)+xoffs,
                                #               cy-self.block_depth//2*(posy+posx-x-y)-self.block_height*(z-posz)+yoffs)
                                #if w == 3:
                                #    self.screen.blit(self.thinwall3_img, rect)
                                #elif w == 5:
                                #    self.screen.blit(self.thinwall5_img, rect)
                                self.screen.blit(self.thinwalls[w], rect)

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

            if event.key == pygame.K_DOWN:
                v.position.x = constrain(v.position.x+1, 0, lv.xsize-1)
            elif event.key == pygame.K_UP:
                v.position.x = constrain(v.position.x-1, 0, lv.xsize-1)
            elif event.key == pygame.K_LEFT:
                v.position.y = constrain(v.position.y+1, 0, lv.ysize-1)
            elif event.key == pygame.K_RIGHT:
                v.position.y = constrain(v.position.y-1, 0, lv.ysize-1)
            elif event.key == pygame.K_PAGEUP:
                v.position.z = constrain(v.position.z+1, 0, lv.zsize-1)
            elif event.key == pygame.K_PAGEDOWN:
                v.position.z = constrain(v.position.z-1, 0, lv.zsize-1)

            elif event.key == pygame.K_SPACE:
                if bl.floor == None:
                    bl.floor = 1
                elif bl.floor == 0.5:
                    bl.floor = None
                elif bl.floor == 1:
                    bl.floor = 0.5


            elif event.key == pygame.K_e:
                direction = 0
            elif event.key == pygame.K_w:
                direction = 1
            elif event.key == pygame.K_q:
                direction = 2
            elif event.key == pygame.K_a:
                direction = 3
            elif event.key == pygame.K_z:
                direction = 4
            elif event.key == pygame.K_x:
                direction = 5
            elif event.key == pygame.K_c:
                direction = 6
            elif event.key == pygame.K_d:
                direction = 7

            if direction > -1:
                if bl.get_wall(direction) is not None:
                    bl.remove_wall(direction)
                else:
                    bl.set_wall(direction, 1)


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
