import pygame
import sys
import numpy as np
from physics.gravity import gravitational_force, escape_velocity
from environment.celestial_objects import CelestialBody, Debris
from ui.dashboard import Dashboard

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

# Load assets
spaceship_img = pygame.image.load("assets/spaceship.png")

# Initialize spacecraft
ship = {
    "x": 640,
    "y": 360,
    "energy": 1e12,
    "velocity": [0, 0]
}

# Generate sample celestial bodies
celestial_bodies = [
    CelestialBody(500, 300, 1.989e30, 50, "star"),      # Sun-like star
    CelestialBody(800, 400, 6.96e24, 20, "planet"),     # Earth-like planet
    CelestialBody(200, 200, 1e31, 30, "blackhole")      # Black hole
]

dashboard = Dashboard(screen)

running = True
while running:
    screen.fill((0, 0, 0))  # Space background
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Calculate gravitational effects
    for body in celestial_bodies:
        dx = body.x - ship["x"]
        dy = body.y - ship["y"]
        distance = np.hypot(dx, dy)
        force = gravitational_force(body.mass, 1e5, distance)  # Ship mass = 1e5 kg
        
        # Update ship velocity (simplified)
        ship["velocity"][0] += force * dx / (distance + 1e-10) * 0.01
        ship["velocity"][1] += force * dy / (distance + 1e-10) * 0.01
    
    # Update ship position
    ship["x"] += ship["velocity"][0]
    ship["y"] += ship["velocity"][1]
    
    # Render
    screen.blit(spaceship_img, (ship["x"], ship["y"]))
    for body in celestial_bodies:
        pygame.draw.circle(screen, (255, 200, 0) if body.type == "star" else (0, 0, 255), (body.x, body.y), body.radius)
    
    dashboard.draw(ship["energy"], celestial_bodies)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()