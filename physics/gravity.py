import numpy as np

G = 6.67430e-11  # Gravitational constant

def gravitational_force(m1, m2, r):
    """Calculate gravitational force between two masses."""
    return G * (m1 * m2) / (r**2 + 1e-10)  # Prevent division by zero

def escape_velocity(mass, radius):
    """Calculate escape velocity from a celestial body."""
    return np.sqrt(2 * G * mass / radius)