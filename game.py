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
        self.subcursor = 0
        self.subcursor_mode=False
        self.subcurpos = Vector(0,0,0)

        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()

        self.block_img = pygame.image.load("block2.png")
        self.block_rect = self.block_img.get_rect()
        self.block_hz = 32
        self.block_wx = 16
        self.block_hx = 16
        self.block_wy = 32
        self.block_hy = 8

        self.cursor_imgs = [pygame.image.load("cursor2_empty.png"),
                            pygame.image.load("cursor2b_empty.png"),
                            pygame.image.load("cursor2c_empty.png"),
                            pygame.image.load("cursor2d_empty.png")]
        for img in self.cursor_imgs:
            img.set_alpha(100)
        self.cursor_full_img = pygame.image.load("cursor2_full.png")
        self.cursor_rect = self.block_img.get_rect()

        self.font = pygame.font.Font(None, 25)

    def get_subcursor_sizes(self):
        d = 2**(self.subcursor)
        return (self.block_wx//d, self.block_hx//d, self.block_wy//d, self.block_hy//d, self.block_hz//d)

    def move_position(self, dx=0, dy=0, dz=0):
        if 0 <= self.position.x+dx < len(self.level.data[0][0]):
            self.position.x += dx
        if 0 <= self.position.y+dy < len(self.level.data[0]):
            self.position.y += dy
        if 0 <= self.position.z+dz < len(self.level.data):
            self.position.z += dz


    def move_subcursor(self, dx=0, dy=0, dz=0):
        scale = 2**(self.subcursor)
        if 0 <= self.subcurpos.x+dx < scale:
            self.subcurpos.x += dx
        elif self.subcurpos.x+dx < 0:
            self.subcurpos.x = scale-1
            self.move_position(dx=-1)
        elif self.subcurpos.x+dx >= scale:
            self.subcurpos.x = 0
            self.move_position(dx=1)

        if 0 <= self.subcurpos.y+dy < scale:
            self.subcurpos.y += dy
        elif self.subcurpos.y+dy < 0:
            self.subcurpos.y = scale-1
            self.move_position(dy=-1)
        elif self.subcurpos.y+dy >= scale:
            self.subcurpos.y = 0
            self.move_position(dy=1)

        if 0 <= self.subcurpos.z+dz < scale:
            self.subcurpos.z += dz
        elif self.subcurpos.z+dz < 0:
            self.subcurpos.z = scale-1
            self.move_position(dz=-1)
        elif self.subcurpos.z+dz >= scale:
            self.subcurpos.z = 0
            self.move_position(dz=1)


    def increase_subcursor_scale(self):
        if self.subcursor+1 <= 3:
            self.subcursor += 1
            self.subcurpos = self.subcurpos * 2

    def decrease_subcursor_scale(self):
        if self.subcursor-1 >= 0:
            self.subcursor -= 1
            self.subcurpos.x = self.subcurpos.x // 2
            self.subcurpos.y = self.subcurpos.y // 2
            self.subcurpos.z = self.subcurpos.z // 2

    def draw(self):
        cx, cy = self.get_screen_center()
        posx, posy, posz = self.position.x, self.position.y, self.position.z
        self.screen.fill(BLACK)
        for z in range(self.level.zsize):
            for y in range(self.level.ysize):
                for x in range(self.level.xsize):
                    block = self.level.get_block((x, y,z))
                    rect=self.block_rect
                    #rect.center = (cx-self.block_width//2*(posx-posy-x+y),
                    #               cy-self.block_depth//2*(posy+posx-x-y)-self.block_height*(z-posz))
                    rect.center = (cx+self.block_wx*(x-posx)-self.block_wy*(y-posy),
                                   cy+self.block_hy*(y-posy)+self.block_hx*(x-posx)-self.block_hz*(z-posz))
                    if self.screen.get_rect().contains(rect):
                        block.draw()
                        self.screen.subsurface(rect).blit(block.surface, (0,0))
                        #self.screen.subsurface(rect).blit(self.block_img, (0,0))
                    if (x, y, z) == (self.position.x, self.position.y, self.position.z):
                        ##print "drawing cursor"
                        rect.center = (cx-self.block_wx*(posx-x)+self.block_wy*(posy-y),
                                        cy-self.block_hy*(posy-y)+self.block_hx*(posx-x)-self.block_hz*(z-posz))

                        self.screen.blit(self.cursor_imgs[0], rect)
                        if self.subcursor > 0:
                            xsub, ysub, zsub = self.subcurpos.tuple()
                            wx, hx, wy, hy, hz = self.get_subcursor_sizes()
                            ###print "rect before:", rect.topleft
                            rect =  rect.move(xsub*wx+(2**self.subcursor-1-ysub)*wy,
                                              ysub*hy+xsub*hx+(2**self.subcursor-1-zsub)*hz)
                            ###print "rect after:", rect.topleft
                            ##print "subcursor:", (x*wx+(2**self.subcursor-1-y)*wy, y*hy+x*hx+(2**self.subcursor-1-z)*hz)

                            self.screen.blit(self.cursor_imgs[self.subcursor], rect)


        ###print v.position
        postext = self.font.render("%d, %d, %d"%v.position.tuple(), 1, (255,255,0))
        self.screen.blit(postext, (10,10))
        pygame.display.flip()

    def get_screen_center(self):
        return self.size[0]//2, self.size[1]//2

lv = data.Level(size=(10,10,10))

b = data.Block(1)

for i in range(10):
    lv.put_block((i,0,0), b)
    lv.put_block((i,2,0), b)
    lv.put_block((0,i,0), b)
    lv.put_block((1,i,1), b)

c=data.Block([1,1,1,0,[1,1,1,0,[1,1,1,0,1,0,0,0],0,0,0],0,0,0])
lv.put_block((3,3,0), c)

#for i in range(100):
#    d.set_random_block(1)

v = View(level=lv)
v.draw()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.KEYDOWN:
            ##print event.key

            if event.key == pygame.K_DOWN:
                if not v.subcursor_mode:
                    v.position.x = constrain(v.position.x+1, 0, lv.xsize-1)
                else:
                    v.move_subcursor(dx=1)
            elif event.key == pygame.K_UP:
                if not v.subcursor_mode:
                    v.position.x = constrain(v.position.x-1, 0, lv.xsize-1)
                else:
                    v.move_subcursor(dx=-1)
            elif event.key == pygame.K_LEFT:
                if not v.subcursor_mode:
                    v.position.y = constrain(v.position.y+1, 0, lv.ysize-1)
                else:
                    v.move_subcursor(dy=1)
            elif event.key == pygame.K_RIGHT:
                if not v.subcursor_mode:
                    v.position.y = constrain(v.position.y-1, 0, lv.ysize-1)
                else:
                    v.move_subcursor(dy=-1)
            elif event.key == pygame.K_PAGEUP:
                if not v.subcursor_mode:
                    v.position.z = constrain(v.position.z+1, 0, lv.zsize-1)
                else:
                    v.move_subcursor(dz=1)
            elif event.key == pygame.K_PAGEDOWN:
                if not v.subcursor_mode:
                    v.position.z = constrain(v.position.z-1, 0, lv.zsize-1)
                else:
                    v.move_subcursor(dz=-1)

            elif event.key == pygame.K_PLUS:
                v.decrease_subcursor_scale()
            elif event.key == pygame.K_MINUS:
                v.increase_subcursor_scale()


            elif event.key == pygame.K_SPACE:
                if not v.subcursor_mode:
                    if lv.get_block(v.position) == 0:
                        lv.put_block(v.position, 1)
                    else:
                        lv.put_block(v.position, 0)

            elif event.key == pygame.K_a:
                print v.subcurpos.tuple()
                lv.get_block(v.position).put_sub_element(v.subcursor, v.subcurpos.tuple(), 1)

            elif event.key == pygame.K_s:
                print v.subcurpos.tuple()
                lv.get_block(v.position).remove_sub_element(v.subcursor, v.subcurpos.tuple())

            elif event.key == pygame.K_RETURN:
                v.subcursor_mode = not v.subcursor_mode

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
