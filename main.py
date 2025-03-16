import pygame
import sys
import numpy as np
from physics.gravity import gravitational_force
from environment.celestial_objects import CelestialBody, Debris
from ui.dashboard import Dashboard

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Stellar Escape")
clock = pygame.time.Clock()

# Load assets
def load_image(path, size=None):
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size) if size else img
    except pygame.error as e:
        print(f"Error loading {path}: {e}")
        sys.exit()

assets = {
    "spaceship": load_image("./assets/spaceship.jpg", (40, 40)),
    "star": load_image("assets/star.png", (100, 100)),
    "planet": load_image("assets/planet.png", (80, 80)),
    "blackhole": load_image("assets/blackhole.jpg", (60, 60)),
    "debris": load_image("assets/debris.jpg", (30, 30))
}

# Initialize spacecraft
ship = {
    "x": 640,
    "y": 360,
    "energy": 1e12,
    "velocity": [0.0, 0.0],
    "thrust": 0.2,
    "mass": 1e5  # kg
}

# Initialize celestial bodies
celestial_bodies = [
    CelestialBody(500, 300, 1.989e30, 50, "Star", assets["star"]),
    CelestialBody(800, 400, 5.97e24, 20, "Planet", assets["planet"]),
    CelestialBody(200, 200, 1e31, 30, "Black Hole", assets["blackhole"])
]

# Initialize debris
debris_objects = [
    Debris(400, 200, [0.3, 0.2], assets["debris"]),
    Debris(600, 500, [-0.2, 0.4], assets["debris"]),
    Debris(300, 400, [0.1, -0.3], assets["debris"])
]

dashboard = Dashboard(screen)

def handle_input():
    keys = pygame.key.get_pressed()
    
    # Thrusters
    if keys[pygame.K_w]:
        ship["velocity"][1] -= ship["thrust"]
        ship["energy"] -= 5e4
    if keys[pygame.K_s]:
        ship["velocity"][1] += ship["thrust"]
        ship["energy"] -= 5e4
    if keys[pygame.K_a]:
        ship["velocity"][0] -= ship["thrust"]
        ship["energy"] -= 5e4
    if keys[pygame.K_d]:
        ship["velocity"][0] += ship["thrust"]
        ship["energy"] -= 5e4

running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Handle input
    handle_input()
    
    # Update physics
    for body in celestial_bodies:
        dx = body.x - ship["x"]
        dy = body.y - ship["y"]
        distance = np.hypot(dx, dy)
        
        if distance < 500:  # Only apply nearby gravity
            force = gravitational_force(body.mass, ship["mass"], distance)
            ship["velocity"][0] += force * dx / (distance + 1e-10) * 0.01
            ship["velocity"][1] += force * dy / (distance + 1e-10) * 0.01
    
    # Update positions
    ship["x"] += ship["velocity"][0]
    ship["y"] += ship["velocity"][1]
    
    # Update debris positions
    for debris in debris_objects:
        debris.x += debris.velocity[0]
        debris.y += debris.velocity[1]
    
    # Keep ship within bounds
    ship["x"] = np.clip(ship["x"], 0, 1280)
    ship["y"] = np.clip(ship["y"], 0, 720)
    
    # Collision detection
    ship_rect = assets["spaceship"].get_rect(center=(ship["x"], ship["y"]))
    for debris in debris_objects:
        debris_rect = debris.image.get_rect(center=(debris.x, debris.y))
        if ship_rect.colliderect(debris_rect):
            ship["energy"] -= 1e6
    
    # Render
    screen.fill((10, 10, 30))  # Dark space background
    
    # Draw celestial bodies
    for body in celestial_bodies:
        img_rect = body.image.get_rect(center=(body.x, body.y))
        screen.blit(body.image, img_rect)
    
    # Draw debris
    for debris in debris_objects:
        img_rect = debris.image.get_rect(center=(debris.x, debris.y))
        screen.blit(debris.image, img_rect)
    
    # Draw spaceship
    screen.blit(assets["spaceship"], (ship["x"], ship["y"]))
    
    # Update dashboard
    dashboard.draw(ship["energy"], ship["velocity"], celestial_bodies)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()