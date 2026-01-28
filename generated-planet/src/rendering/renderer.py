"""Renderer module - handles all drawing operations"""

import pygame
from typing import List, Dict
from ..utils.vectors import Vector3
from .camera import Camera
from .sprites import draw_3d_animal_sprite, draw_energy_bar, draw_breeding_indicator, draw_terrain_block
from ..utils.constants import BLOCK_COLORS, WINDOW_WIDTH, WINDOW_HEIGHT, BlockType

class Renderer:
    """Main rendering engine"""
    
    def __init__(self, screen: pygame.Surface, camera: Camera):
        self.screen = screen
        self.camera = camera
    
    def clear(self, color: tuple = (135, 206, 235)):
        """Clear screen with color"""
        self.screen.fill(color)
    
    def render_terrain(self, planet):
        """Render all visible terrain blocks"""
        visible_blocks = planet.get_visible_blocks(self.camera.position)
        
        # Sort by distance for proper rendering
        visible_blocks.sort(key=lambda b: (b[0] + b[1] + b[2]), reverse=True)
        
        for x, y, z, block_type in visible_blocks:
            if block_type == BlockType.AIR:
                continue
            
            block_pos = Vector3(x + 0.5, y + 0.5, z + 0.5)
            projected = self.camera.project_3d_to_2d(block_pos)
            
            if projected:
                x_2d, y_2d, scale = projected
                if 0 <= x_2d < WINDOW_WIDTH and 0 <= y_2d < WINDOW_HEIGHT:
                    size = max(2, int(4 * scale))
                    color = BLOCK_COLORS.get(block_type, (100, 100, 100))
                    draw_terrain_block(self.screen, x_2d, y_2d, size, color)
    
    def render_animals(self, animals: List):
        """Render all animals"""
        for animal in animals:
            projected = self.camera.project_3d_to_2d(animal.position)
            
            if projected:
                x_2d, y_2d, scale = projected
                if 0 <= x_2d < WINDOW_WIDTH and 0 <= y_2d < WINDOW_HEIGHT and scale > 0:
                    size = max(5, int(7 * scale))
                    
                    # Draw 3D sprite
                    draw_3d_animal_sprite(self.screen, x_2d, y_2d, size, animal.color, animal.animal_type, scale)
                    
                    # Draw energy bar
                    energy_pct = min(1.0, animal.energy / animal.max_energy)
                    draw_energy_bar(self.screen, x_2d, y_2d, size, energy_pct)
                    
                    # Draw breeding indicator
                    if animal.is_breeding:
                        draw_breeding_indicator(self.screen, x_2d, y_2d, size)
    
    def render_scene(self, planet, animals: List):
        """Render complete scene"""
        self.clear()
        self.render_terrain(planet)
        self.render_animals(animals)
    
    def update_display(self):
        """Update display"""
        pygame.display.flip()
