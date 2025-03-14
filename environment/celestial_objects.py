class CelestialBody:
    def __init__(self, x, y, mass, radius, type):
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius
        self.type = type  # "star", "planet", "blackhole"

class Debris:
    def __init__(self, x, y, velocity):
        self.x = x
        self.y = y
        self.velocity = velocity