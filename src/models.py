import math


class System:
    def __init__(self, charges=[]):
        self.particles = charges

    def add_particles(self, particle):
        assert isinstance(particle, Particle)

        self.particles.append(Particle)

    def get_particles(self):
        return self.particles

    def distance(a, b):
        return math.sqrt(sum([(x1 - x2)**2 for x1, x2 in zip(a, b)]))

    def get_force(self, x, y, k=9e9):
        force = [0, 0]
        # return k * force[1] * 
        # TODO: Add calculations for electric field


class Particle:
    def __init__(self, x, y, charge=1):
        self.charge = charge
        self.x = x
        self.y = y
