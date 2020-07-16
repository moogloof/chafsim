import math
import numpy as np


# System class
class System:
    def __init__(self, charges=[], conversion=100):
        # Particles in system
        self._particles = charges
        self.conversion = conversion

    def add_particle(self, particle):
        # Check if particle is an instance of Particle class
        assert isinstance(particle, Particle)

        # Add particle
        self._particles.append(particle)

    # Return all particles
    def get_particles(self):
        return self._particles

    # Return distance between two coordinates, a and b
    def distance(self, a, b):
        return math.sqrt(sum([(x1 - x2)**2 for x1, x2 in zip(a, b)]))

    # Return field at a position given the k
    def get_field(self, x, y, k=9e9):
        # Field vector
        field_v = [0, 0]

        # Find net field at a position
        for particle in self._particles:
            # Get the position of the particle
            particle_pos = (particle.x, particle.y)

            # Get distance to particle
            dist = self.distance((x, y), (particle.x, particle.y)) / self.conversion

            # Get field magnitude
            try:
                mag = k * particle.charge / (dist ** 2)
            except ZeroDivisionError:
                # Return false if the particle and the coordinates are in the same position
                return False

            # Calculate components of field vector
            field_v[0] += (mag/dist) * (particle.x - x)
            field_v[1] += (mag/dist) * (particle.y - y)

        # Return the field vector
        return field_v


# Particle class
class Particle:
    def __init__(self, x, y, charge=1):
        # Charge of particle
        self.charge = charge

        # Coordinates of particle
        self.x = x
        self.y = y

        # Particle id
        self.id = None
