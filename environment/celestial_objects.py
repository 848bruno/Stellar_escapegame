class CelestialBody:
    def __init__(self, x, y, mass, radius, body_type, image):
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius
        self.type = body_type
        self.image = image

class Debris:
    def __init__(self, x, y, velocity, image):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.image = image