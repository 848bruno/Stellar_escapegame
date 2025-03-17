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

def load_image(path, size=None):
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size) if size else img
    except pygame.error as e:
        print(f"Error loading {path}: {e}")
        sys.exit()

assets = {
    "bg": load_image("assets/space_bg.png", (1280, 720)),
    "spaceship": load_image("assets/spaceship.jpg", (40, 40)),
    "star": load_image("assets/star.png", (100, 100)),
    "planet": load_image("assets/planet.png", (80, 80)),
    "blackhole": load_image("assets/blackhole.jpg", (60, 60)),
    "debris": load_image("assets/debris.jpg", (30, 30))
}

# Ship initialization with proper position handling
ship = {
    "x": 640.0,
    "y": 360.0,
    "energy": 1e12,
    "velocity": [0.0, 0.0],
    "thrust": 0.8,
    "mass": 1e5,
    "rect": pygame.Rect(0, 0, 40, 40)  # Empty rect, will be updated
}

celestial_bodies = [
    CelestialBody(500, 300, 1.989e30, 50, "Star", assets["star"]),
    CelestialBody(800, 400, 5.97e24, 20, "Planet", assets["planet"]),
    CelestialBody(200, 200, 1e31, 30, "Black Hole", assets["blackhole"])
]

debris_objects = [
    Debris(400.0, 200.0, [0.3, 0.2], assets["debris"]),
    Debris(600.0, 500.0, [-0.2, 0.4], assets["debris"]),
    Debris(300.0, 400.0, [0.1, -0.3], assets["debris"])
]

dashboard = Dashboard(screen)

def handle_input():
    keys = pygame.key.get_pressed()
    thrust_active = False
    
    if ship["energy"] > 0:
        if keys[pygame.K_w]:
            ship["velocity"][1] -= ship["thrust"]
            thrust_active = True
        if keys[pygame.K_s]:
            ship["velocity"][1] += ship["thrust"]
            thrust_active = True
        if keys[pygame.K_a]:
            ship["velocity"][0] -= ship["thrust"]
            thrust_active = True
        if keys[pygame.K_d]:
            ship["velocity"][0] += ship["thrust"]
            thrust_active = True
    
    if thrust_active:
        ship["energy"] -= 3e4

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    handle_input()
    
    # Physics calculations
    for body in celestial_bodies:
        dx = body.x - ship["x"]
        dy = body.y - ship["y"]
        distance = np.hypot(dx, dy)
        
        if distance < 500 and distance > 10:  # Add minimum distance
            force = gravitational_force(body.mass, ship["mass"], distance)
            ship["velocity"][0] += force * dx / (distance + 1e-10) * 0.01
            ship["velocity"][1] += force * dy / (distance + 1e-10) * 0.01
    
    # Update position with screen wrapping first
    ship["x"] += ship["velocity"][0]
    ship["y"] += ship["velocity"][1]
    ship["x"] %= 1280  # Wrap around before rect update
    ship["y"] %= 720
    
    # Update rect with clamped integer values
    ship["rect"].center = (
        int(np.clip(ship["x"], 0, 1280)),
        int(np.clip(ship["y"], 0, 720))
    )
    
    # Update debris with proper wrapping
    for debris in debris_objects:
        debris.x += debris.velocity[0]
        debris.y += debris.velocity[1]
        debris.x %= 1280
        debris.y %= 720
    
    # Collision detection with integer positions
    ship_rect = assets["spaceship"].get_rect(center=ship["rect"].center)
    for debris in debris_objects:
        debris_rect = debris.image.get_rect(
            center=(int(debris.x), int(debris.y)))
        if ship_rect.colliderect(debris_rect):
            ship["energy"] -= 2e6
            debris.x, debris.y = np.random.uniform(0, 1280, 2)
    
    # Rendering
    screen.blit(assets["bg"], (0, 0))
    
    for body in celestial_bodies:
        screen.blit(body.image, body.image.get_rect(center=(body.x, body.y)))
    
    for debris in debris_objects:
        screen.blit(debris.image, debris.image.get_rect(
            center=(int(debris.x), int(debris.y))))
    
    # Rotate spaceship
    if np.linalg.norm(ship["velocity"]) > 0.1:
        angle = np.degrees(np.arctan2(-ship["velocity"][1], ship["velocity"][0])) - 90
        rotated_ship = pygame.transform.rotate(assets["spaceship"], angle)
    else:
        rotated_ship = assets["spaceship"]
    
    screen.blit(rotated_ship, rotated_ship.get_rect(center=ship["rect"].center))
    
    dashboard.draw(ship["energy"], ship["velocity"], celestial_bodies)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()