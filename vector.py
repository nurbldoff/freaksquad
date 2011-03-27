#from __future__ import division

from math import *

class Vector(object):
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def __index__(self, n):
        if n == 0:
            return self.x
        elif n == 1:
            return self.y
        elif n == 2:
            return self.z

    def tuple(self):
        return (self.x, self.y, self.z)

    def norm(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def __mul__(self, t):
        return Vector(t*self.x, t*self.y, t*self.z)

    def __rmul__(self, t):
        return self*t

    def __truediv__(self, t):   # must be named this to work with future-division
        return Vector(self.x/t, self.y/t, self.z/t)

    def __div__(self, t):
        return Vector(self.x/t, self.y/t, self.z/t)

    def __rdiv__(self, t):
        return Vector(self.x/t, self.y/t, self.z/t)

    def normalized(self):
        return self/self.norm()
        #self.norm()

    def __add__(self, v):
        return Vector(self.x+v.x, self.y+v.y, self.z+v.z)

    def __sub__(self, v):
        return self+(-v)

    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)

    def __cmp__(self, v):
        #if self.x==v.x and self.y==v.y and self.z==v.z: return 0
        if (self-v).norm() < 1e-10:   # This is just a guess...
            return 0
        else: return 1

    def __repr__(self):
        return "(%f, %f, %f)"%(self.x, self.y, self.z)

    def scalar(self, v):
        return self.x*v.x + self.y*v.y + self.z*v.z

    def cross(self, v):
        return Vector(self.y*v.z-self.z*v.y,
                      self.z*v.x-self.x*v.z,
                      self.x*v.y-self.y*v.x)

    def rotate(self, theta):
        xtheta, ytheta, ztheta = theta.x, theta.y, theta.z
        # rotate around x-axis
        xp = self.x
        yp = self.y*cos(xtheta)-self.z*sin(xtheta)
        zp = self.z*cos(xtheta)+self.y*sin(xtheta)

        # ...y-axis
        xpp = xp*cos(ytheta)+zp*sin(ytheta)
        ypp = yp
        zpp = zp*cos(ytheta)-xp*sin(ytheta)

        # ...and z-axis
        xppp = xpp*cos(ztheta) - ypp*sin(ztheta)
        yppp = ypp*cos(ztheta) + xpp*sin(ztheta)
        zppp = zpp

        return Vector(xppp, yppp, zppp)

    def rotate_around(self, u, theta):
        # Some time saving intermediates
        ux2 = u.x**2
        uy2 = u.y**2
        uz2 = u.z**2
        c = cos(theta)
        s = sin(theta)

        # Rotation matrix elements
        R11 = ux2+(1-ux2)*c
        R12 = u.x*u.y*(1-c)-u.z*s
        R13 = u.x*u.z*(1-c)+u.y*s

        R21 = u.x*u.y*(1-c)+u.z*s
        R22 = uy2+(1-uy2)*c
        R23 = u.y*u.z*(1-c)-u.x*s

        R31 = u.x*u.z*(1-c)-u.y*s
        R32 = u.y*u.z*(1-c)+u.x*s
        R33 = uz2+(1-uz2)*c

        #print (R11, R12, R13)
        #print (R21, R22, R23)
        #print (R31, R32, R33)

        # Matrix-vector multiplication
        vx = R11*self.x + R12*self.y + R13*self.z
        vy = R21*self.x + R22*self.y + R23*self.z
        vz = R31*self.x + R32*self.y + R33*self.z

        #print (vx, vy, vz)

        return Vector(vx, vy, vz)
