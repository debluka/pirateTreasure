import pygame

from GameSettings import gameSettings


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def scaleRect(rect: pygame.Rect) -> pygame.Rect:
    rect.x = rect.x * gameSettings.w_scale
    rect.width = rect.width * gameSettings.w_scale
    rect.y = rect.y * gameSettings.h_scale
    rect.height = rect.height * gameSettings.h_scale

    return rect


def scaleSurface(img: pygame.Surface, srcImg: pygame.Surface) -> pygame.Surface:
    return pygame.transform.scale(srcImg, (img.get_width() * gameSettings.w_scale,
                                           img.get_height() * gameSettings.h_scale))


def scaleRectBase(rect: pygame.Rect) -> pygame.Rect:
    rect.x = rect.x * gameSettings.w_scale_base
    rect.width = rect.width * gameSettings.w_scale_base
    rect.y = rect.y * gameSettings.h_scale_base
    rect.height = rect.height * gameSettings.h_scale_base

    return rect


def scaleSurfaceBase(img: pygame.Surface) -> pygame.Surface:
    return pygame.transform.scale(img, (img.get_width() * gameSettings.w_scale_base,
                                        img.get_height() * gameSettings.h_scale_base))
