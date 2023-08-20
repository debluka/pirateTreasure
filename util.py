import pygame

from GameSettings import gameSettings
from MainGameState import mainGameState


def collide(obj1: any, obj2: any) -> tuple[int, int] | None:
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y - mainGameState.yOffset
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None

def collide1(obj1: any, obj2: any) -> tuple[int, int] | None:
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

def gradientRect( window, left_colour, right_colour, target_rect ):
    """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
    colour_rect = pygame.Surface( ( 2, 2 ) )                                   # tiny! 2x2 bitmap
    pygame.draw.line( colour_rect, left_colour,  ( 0,0 ), ( 0,1 ) )            # left colour line
    pygame.draw.line( colour_rect, right_colour, ( 1,0 ), ( 1,1 ) )            # right colour line
    colour_rect = pygame.transform.smoothscale( colour_rect, ( target_rect.width, target_rect.height ) )  # stretch!
    window.blit( colour_rect, target_rect )                                    # paint it

def circle_rect_collision(circle_center, circle_radius, rect: pygame.Rect):
    rect_center = rect.center
    dx = abs(circle_center[0] - rect_center[0])
    dy = abs(circle_center[1] - rect_center[1])

    if dx > (rect.width / 2 + circle_radius):
        return False
    if dy > (rect.height / 2 + circle_radius):
        return False
    if dx <= (rect.width / 2):
        return True
    if dy <= (rect.height / 2):
        return True

def line_rect_collision(line_start, line_end, rect):
    rect_left = rect.left
    rect_right = rect.right
    rect_top = rect.top
    rect_bottom = rect.bottom

    # Check if any of the line's endpoints are inside the rectangle
    if rect.collidepoint(line_start) or rect.collidepoint(line_end):
        return True

    # Check for line intersection with each side of the rectangle
    if (line_start[0] > rect_right and line_end[0] > rect_right) or \
       (line_start[0] < rect_left and line_end[0] < rect_left) or \
       (line_start[1] > rect_bottom and line_end[1] > rect_bottom) or \
       (line_start[1] < rect_top and line_end[1] < rect_top):
        return False

    return True