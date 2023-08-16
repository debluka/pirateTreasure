import math

import pygame

from MainGameState import mainGameState
from Textures import EXPLOSION1, EXPLOSION2, EXPLOSION3
from util import scaleSurfaceBase, scaleSurface


class ExplosionAnimation:
    def __init__(self, x: int, y: int, window: pygame.Surface):
        self.x: int = x
        self.y: int = y
        self.window: pygame.Surface = window

        self.frameSpeed: int = 5
        self.animationCounter: int = 0
        self.looping: bool = False
        self.isDone: bool = False

        self.srcFrames: (pygame.Surface, ...) = (scaleSurfaceBase(EXPLOSION1), scaleSurfaceBase(EXPLOSION2), scaleSurfaceBase(EXPLOSION3))
        self.frames: (pygame.Surface, ...) = self.srcFrames
        self.currentFrame: pygame.Surface = self.frames[0]

    def update(self):
        self.currentFrame = scaleSurfaceBase(self.frames[math.floor((self.animationCounter % (self.frameSpeed * len(self.frames)) / self.frameSpeed))])
        self.animationCounter += 1

        if self.animationCounter == len(self.frames * self.frameSpeed):
            self.isDone = True

    def draw(self):
        if self.animationCounter < self.frameSpeed * len(self.frames):
            self.window.blit(self.currentFrame, (self.x - self.currentFrame.get_width() / 2,
                                                 self.y - self.currentFrame.get_height() / 2 + mainGameState.yOffset,
                                                 self.currentFrame.get_width(),
                                                 self.currentFrame.get_height()))
