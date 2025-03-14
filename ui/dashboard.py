import pygame

class Dashboard:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
    
    def draw(self, ship_energy, nearby_objects):
        # Display energy status
        energy_text = self.font.render(f"Energy: {ship_energy:.2f} J", True, (255, 255, 255))
        self.screen.blit(energy_text, (10, 10))
        
        # Display nearby objects
        y_offset = 40
        for obj in nearby_objects:
            obj_text = self.font.render(f"{obj.type} - Mass: {obj.mass} kg", True, (255, 255, 255))
            self.screen.blit(obj_text, (10, y_offset))
            y_offset += 20