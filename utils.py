def constrain(value, minlim, maxlim):
    "Return the value if it lies between max and min inclusive, otherwise return the closest of max ang min."
    return max(minlim, min(maxlim, value))

def rotate_xypos(x, y, xmax, ymax, n):
    if n == 0:
        return x, y
    elif n == 1:
        return ymax-y, x
    elif n == 2:
        return xmax-x, ymax-y
    elif n == 3:
        return y, xmax-x

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


def texture_wall(surf, texture, direction, thickness):
    """
    Cuts the appropriate parts from a cube texture to build a wall section.
    """
    leftwall, rightwall, top = texture
    srect = surf.get_rect()
    if direction == 0:
        trect = leftwall.get_rect()
        trect.width = thickness*2
        surf.blit(leftwall, (srect.width/2-thickness*2, -srect.width/4+thickness), trect)
        trect.left = srect.width - thickness*2
        surf.blit(rightwall, (srect.width/2, -srect.width/4+thickness), trect)

    if direction == 1:
        trect = leftwall.get_rect()
        trect.width = srect.width/2 - 2*thickness*2
        trect.left = srect.width/2+thickness*2
        surf.blit(rightwall, (2*thickness*2, -srect.width/4+thickness),trect)
        trect.left = 0
        trect.width = thickness*2
        surf.blit(leftwall, (thickness*2, -thickness), trect)

    if direction == 2:
        trect = leftwall.get_rect()
        trect.width = thickness*2
        surf.blit(leftwall, (0,0), trect)
        trect.left = srect.width/2
        surf.blit(rightwall, (thickness*2, -srect.width/4+thickness), trect)

    if direction == 3:
        trect = leftwall.get_rect()
        trect.width = srect.width/2 - 2*thickness*2
        trect.left = thickness*2
        surf.blit(leftwall, (thickness*2, 0), trect)
        trect.left = srect.width/2
        trect.width = thickness*2
        surf.blit(rightwall, (srect.width/2-thickness*2, -thickness), trect)

    if direction == 4:
        trect = leftwall.get_rect()
        trect.width = thickness*2
        trect.left = srect.width/2 - 2*thickness
        surf.blit(leftwall, trect.topleft, trect)
        trect.left = srect.width/2
        surf.blit(rightwall, trect.topleft, trect)


    if direction == 5:
        trect = leftwall.get_rect()
        trect.width = srect.width/2 - 2*thickness*2
        trect.left = srect.width/2+thickness*2
        surf.blit(rightwall, (srect.width/2+thickness*2, 0), trect)
        trect.left = srect.width/2-thickness*2
        trect.width = thickness*2
        surf.blit(leftwall, (srect.width/2, -thickness), trect)

    if direction == 6:
        trect = leftwall.get_rect()
        trect.width = thickness*2
        trect.left = srect.width/2 - 2*thickness
        surf.blit(leftwall, (srect.width-2*2*thickness, -srect.width/4+thickness), trect)
        trect.left = srect.width - thickness*2
        surf.blit(rightwall, trect.topleft, trect)

    if direction == 7:
        trect = leftwall.get_rect()
        trect.width = srect.width/2 - 2*thickness*2
        trect.left = thickness*2
        surf.blit(leftwall, (srect.width/2, -srect.width/4+thickness), trect)
        trect.width = srect.width/2
        trect.left = srect.width-thickness*2
        surf.blit(rightwall, (srect.width-2*thickness*2, -thickness), trect)


