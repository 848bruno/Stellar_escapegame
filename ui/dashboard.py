import pygame

class Dashboard:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
    
    def draw(self, ship_energy, velocity, nearby_objects):
        # Energy status
        energy_text = self.font.render(f"Energy: {ship_energy:.2e} J", True, (255, 255, 255))
        self.screen.blit(energy_text, (10, 10))
        
        # Velocity display
        vel_text = self.font.render(f"Velocity: X:{velocity[0]:.2f} Y:{velocity[1]:.2f}", True, (255, 255, 255))
        self.screen.blit(vel_text, (10, 40))
        
        # Nearby objects
        y_offset = 70
        for obj in nearby_objects:
            obj_text = self.font.render(
                f"{obj.type} - Mass: {obj.mass:.2e} kg", 
                True, 
                (255, 255, 255)
            )
            self.screen.blit(obj_text, (10, y_offset))
            y_offset += 20