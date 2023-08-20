import random

import pygame

from GameSettings import gameSettings
from MainGameState import mainGameState
from util import circle_rect_collision


class ParticlePrinciple:
	def __init__(self, window: pygame.Surface):
		self.particles: [WaterParticle] = []
		self.window: pygame.Surface = window
		self.counter: int = 0

	def update(self):
		if self.particles:
			self.delete_particles()
			for particle in self.particles:
				particle.update()

	def draw(self):
		for particle in self.particles:
			particle.draw()


	def add_particles(self, x: float, y: float, yDirection: int):
		particle: WaterParticle = WaterParticle(x, y, 5, random.randrange(3 * yDirection if yDirection < 0 else 0, 3 * yDirection if yDirection > 0 else 0), random.randrange(-2, 2), self.window)
		self.particles.append(particle)

	def delete_particles(self):
		particle_copy = [particle for particle in self.particles if particle.radius > 0]
		self.particles = particle_copy


class WaterParticle:
	def __init__(self, x: float, y: float, radius: float, yVelocity: float, xVelocity: float, window: pygame.Surface):
		self.x: float = x
		self.y: float = y
		self.radius: float = radius * gameSettings.w_scale_base
		self.yVelocity: float = yVelocity * gameSettings.w_scale_base
		self.xVelocity: float = xVelocity * gameSettings.w_scale_base
		self.window: pygame.Surface = window

	def update(self):
		self.yVelocity += 0.2 * gameSettings.w_scale_base
		self.x += self.xVelocity
		self.y += self.yVelocity
		self.radius -= 0.15 * gameSettings.w_scale_base

	def draw(self):
		if circle_rect_collision((self.x, self.y), self.radius, mainGameState.cameraRect):
			pygame.draw.circle(self.window, pygame.Color('White'), (self.x, self.y), self.radius)

