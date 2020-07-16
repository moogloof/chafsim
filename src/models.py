import math
import numpy as np


class System:
    def __init__(self, charges=[]):
        self.particles = charges

    def add_particles(self, particle):
        assert isinstance(particle, Particle)

        self.particles.append(Particle)

    def get_particles(self):
        return self.particles

    def distance(self, a, b):
        return math.sqrt(sum([(x1 - x2)**2 for x1, x2 in zip(a, b)]))

    def get_field(self, x, y, k=9e9):
        force = [0, 0]
        for particle in self.particles:
            particle_pos = (particle.x, particle.y)

            dist = self.distance((x, y), (particle.x, particle.y))

            try:
                mag = k * particle.charge / (dist ** 2)
            except ZeroDivisionError:
                return False

            force[0] += (mag/dist) * (particle.x - x)
            force[1] += (mag/dist) * (particle.y - y)

        return force


class Particle:
    def __init__(self, x, y, charge=1):
        self.charge = charge
        self.x = x
        self.y = y
