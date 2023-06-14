import pygame

from GameSettings import gameSettings
from Laser import Laser


class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, velocity, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.effects = dict()
        self.cool_down_counter = 0
        self.base_velocity = velocity
        self.velocity = velocity

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(gameSettings.height):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                # Apply laser effects
                match self.color:
                    case 'red':
                        obj.effects['vulnerable'] = gameSettings.FPS * 3
                    case 'green':
                        obj.effects['poisoned'] = gameSettings.FPS * 3
                    case 'blue':
                        obj.effects['slowed'] = gameSettings.FPS * 3
                obj.health -= 10
                self.lasers.remove(laser)

    def updateEffects(self):
        for effect, duration in self.effects.items():
            if (duration > 0):
                self.effects[effect] = duration - 1
                match effect:
                    case 'slowed':
                        self.velocity = self.base_velocity * 0.6 if duration > 1 else 5
                    case 'poisoned':
                        if duration % 10 == 0:
                            self.health = self.health - 1


    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x + self.get_width()/2 - self.laser_img.get_width()/2, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()
