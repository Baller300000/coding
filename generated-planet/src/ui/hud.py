"""UI rendering module - handles HUD and interface"""

import pygame
from ..utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT

class HUD:
    """Head-up display for simulation information"""
    
    def __init__(self, font: pygame.font.Font):
        self.font = font
        self.small_font = pygame.font.Font(None, 16)
    
    def draw_info(self, surface: pygame.Surface, fps: int, time_seconds: int, 
                  total_animals: int, animal_counts: dict, paused: bool, breeding_count: int):
        """Draw main info panel"""
        info = [
            f"FPS: {fps} | Time: {time_seconds}s | Breeding: {breeding_count}",
            f"Total Animals: {total_animals} | Status: {'PAUSED' if paused else 'RUNNING'}",
        ]
        
        y_offset = 10
        for i, text in enumerate(info):
            text_surface = self.font.render(text, True, (0, 0, 0))
            surface.blit(text_surface, (10, y_offset + i * 22))
    
    def draw_species_list(self, surface: pygame.Surface, animal_counts: dict, start_y: int = 60):
        """Draw list of species and counts"""
        text_surface = self.font.render("Species:", True, (50, 50, 50))
        surface.blit(text_surface, (10, start_y))
        
        y_offset = start_y + 25
        for atype, count in sorted(animal_counts.items()):
            text = f"  {atype}: {count}"
            text_surface = self.small_font.render(text, True, (0, 0, 0))
            surface.blit(text_surface, (10, y_offset))
            y_offset += 18
        
        return y_offset
    
    def draw_controls(self, surface: pygame.Surface, start_y: int):
        """Draw control instructions"""
        text_surface = self.font.render("Controls:", True, (50, 50, 50))
        surface.blit(text_surface, (10, start_y))
        
        controls = [
            "WASD - Move | SPACE/SHIFT - Up/Down | P - Pause",
            "Arrow Keys - Rotate | R/F - Tilt | H - Toggle Info",
            "UP/DOWN - Zoom | Magenta circle = Breeding",
        ]
        
        y_offset = start_y + 25
        for ctrl in controls:
            text_surface = self.small_font.render(ctrl, True, (0, 0, 0))
            surface.blit(text_surface, (10, y_offset))
            y_offset += 18

class Minimap:
    """Optional minimap display"""
    
    def __init__(self, width: int = 150, height: int = 150):
        self.width = width
        self.height = height
        self.x = WINDOW_WIDTH - width - 10
        self.y = 10
    
    def draw(self, surface: pygame.Surface, camera_pos, animals, planet):
        """Draw minimap in corner"""
        # Background
        pygame.draw.rect(surface, (50, 50, 50), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, (200, 200, 200), (self.x, self.y, self.width, self.height), 2)
        
        # Scale factor
        scale = self.width / 100  # 100 unit world
        
        # Draw animals
        for animal in animals:
            px = int(self.x + (animal.position.x + 50) * scale)
            py = int(self.y + (animal.position.z + 50) * scale)
            
            if 0 <= px < self.x + self.width and 0 <= py < self.y + self.height:
                pygame.draw.circle(surface, animal.color, (px, py), 2)
        
        # Draw camera
        cam_x = int(self.x + (camera_pos.x + 50) * scale)
        cam_y = int(self.y + (camera_pos.z + 50) * scale)
        pygame.draw.circle(surface, (0, 255, 0), (cam_x, cam_y), 4)
        pygame.draw.circle(surface, (0, 255, 0), (cam_x, cam_y), 4, 2)

class Stats:
    """Statistics panel"""
    
    def __init__(self, font: pygame.font.Font):
        self.font = font
        self.history = []  # Track population over time
    
    def update(self, animal_counts: dict):
        """Update history with current stats"""
        self.history.append(dict(animal_counts))
        if len(self.history) > 300:
            self.history.pop(0)
    
    def draw_summary(self, surface: pygame.Surface, animal_counts: dict, start_y: int):
        """Draw summary statistics"""
        text_surface = self.font.render("Statistics:", True, (50, 50, 50))
        surface.blit(text_surface, (10, start_y))
        
        herbivore_count = sum(animal_counts.get(f"herbivore_{t}", 0) for t in ["rabbit", "deer", "mouse"])
        carnivore_count = sum(animal_counts.get(f"carnivore_{t}", 0) for t in ["wolf", "fox", "eagle"])
        
        y_offset = start_y + 25
        stats_text = [
            f"Total: {sum(animal_counts.values())}",
            f"Avg Age: N/A",  # Could calculate
            f"Herbivores: {herbivore_count}",
            f"Carnivores: {carnivore_count}",
        ]
        
        for stat in stats_text:
            text_surface = self.font.render(stat, True, (0, 0, 0))
            surface.blit(text_surface, (10, y_offset))
            y_offset += 22
