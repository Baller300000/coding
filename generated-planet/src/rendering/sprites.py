"""Sprite rendering module - handles all sprite drawing"""

import pygame

def draw_3d_animal_sprite(surface: pygame.Surface, x: int, y: int, size: int, color: tuple, animal_type: str, scale_val: float):
    """Draw 3D-looking animal sprite with depth"""
    # Main body (base)
    body_x, body_y = x, y
    body_size = int(size * 1.2)
    pygame.draw.ellipse(surface, color, (body_x - body_size, body_y - size//3, body_size * 2, size))
    
    # Head (darker shade for 3D effect)
    head_color = tuple(max(0, c - 30) for c in color)
    head_size = int(size * 0.6)
    pygame.draw.circle(surface, head_color, (body_x, body_y - size//2), head_size)
    
    # Eyes
    if size > 5:
        eye_color = (0, 0, 0)
        pygame.draw.circle(surface, eye_color, (body_x - head_size//3, body_y - size//2), max(1, int(size//6)))
        pygame.draw.circle(surface, eye_color, (body_x + head_size//3, body_y - size//2), max(1, int(size//6)))
        
        # Eye highlights
        pygame.draw.circle(surface, (255, 255, 255), (body_x - head_size//3 + 1, body_y - size//2 - 1), 1)
        pygame.draw.circle(surface, (255, 255, 255), (body_x + head_size//3 + 1, body_y - size//2 - 1), 1)
    
    # Legs (bottom)
    leg_height = int(size * 0.5)
    leg_color = tuple(max(0, c - 50) for c in color)
    pygame.draw.line(surface, leg_color, (body_x - size//3, body_y + size//2), (body_x - size//3, body_y + size//2 + leg_height), 2)
    pygame.draw.line(surface, leg_color, (body_x + size//3, body_y + size//2), (body_x + size//3, body_y + size//2 + leg_height), 2)
    
    # Special features
    if "eagle" in animal_type.lower() or "bird" in animal_type.lower():
        # Wings
        pygame.draw.line(surface, color, (body_x - body_size - 2, body_y), (body_x - body_size - 6, body_y - 3), 2)
        pygame.draw.line(surface, color, (body_x + body_size + 2, body_y), (body_x + body_size + 6, body_y - 3), 2)
    
    if "wolf" in animal_type.lower() or "fox" in animal_type.lower():
        # Ears
        pygame.draw.polygon(surface, color, [(body_x - head_size//2, body_y - size - 2), 
                                             (body_x - head_size//3, body_y - size//2 - 2),
                                             (body_x - head_size//2, body_y - size//2)])
        pygame.draw.polygon(surface, color, [(body_x + head_size//2, body_y - size - 2), 
                                             (body_x + head_size//3, body_y - size//2 - 2),
                                             (body_x + head_size//2, body_y - size//2)])
    
    if "fish" in animal_type.lower():
        # Tail
        pygame.draw.line(surface, color, (body_x + body_size, body_y), (body_x + body_size + 8, body_y - 3), 2)
        pygame.draw.line(surface, color, (body_x + body_size, body_y), (body_x + body_size + 8, body_y + 3), 2)

def draw_energy_bar(surface: pygame.Surface, x: int, y: int, size: int, energy_pct: float):
    """Draw energy bar under animal"""
    bar_width = size + 4
    bar_height = 2
    
    pygame.draw.rect(surface, (50, 50, 50), (x - bar_width // 2, y + size + 8, bar_width, bar_height))
    
    if energy_pct > 0.5:
        color = (0, 255, 0)
    elif energy_pct > 0.2:
        color = (255, 165, 0)
    else:
        color = (255, 0, 0)
    
    pygame.draw.rect(surface, color, (x - bar_width // 2, y + size + 8, int(bar_width * energy_pct), bar_height))

def draw_breeding_indicator(surface: pygame.Surface, x: int, y: int, size: int):
    """Draw magenta circle around breeding animal"""
    pygame.draw.circle(surface, (255, 0, 255), (x, y), size + 5, 2)

def draw_terrain_block(surface: pygame.Surface, x: int, y: int, size: int, color: tuple):
    """Draw a terrain block"""
    pygame.draw.rect(surface, color, (x - size, y - size, size * 2, size * 2))
    pygame.draw.rect(surface, (0, 0, 0), (x - size, y - size, size * 2, size * 2), 1)
