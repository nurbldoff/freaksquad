import pygame

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


def blit_mask(source, dest, destpos, mask, maskrect):
    tmp = source.copy()
    tmp.blit(mask, maskrect.topleft, maskrect, special_flags=pygame.BLEND_RGBA_MULT)
    #mrect = mask.get_rect()
    #mrect.topleft = maskpos
    dest.blit(tmp, destpos, dest.get_rect().clip(maskrect))

def clip_masks(masks, positions):
    "return the intersection of several masks"
    tmp = masks[0].copy()
    rect = tmp.get_rect()
    frect = rect.copy()
    for m, p in zip(masks, positions):
        tmp.blit(m, p, special_flags=pygame.BLEND_RGBA_MULT)
        tmprect = rect.copy()
        tmprect.topleft = p
        frect = frect.clip(tmprect)
    return tmp, frect

def darken(surf, amount):
    darksurf = surf.copy().convert_alpha()
    darksurf.fill((255-amount, 255-amount, 255-amount), special_flags=pygame.BLEND_RGBA_MAX)
    tmp = surf.copy()
    tmp.blit(darksurf, (0,0), special_flags=pygame.BLEND_RGB_MULT)
    return tmp
