"""Visual effects system"""

import pygame
import random
import math
from typing import List, Tuple

class Particle:
    """A single particle for effects"""
    
    def __init__(self, x: float, y: float, vx: float, vy: float, 
                 color: tuple, lifetime: int, size: int = 2):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
    
    def update(self):
        """Update particle position"""
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        self.vy += 0.1  # gravity
    
    def draw(self, surface: pygame.Surface):
        """Draw particle with fading alpha"""
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        color = tuple(min(255, c) for c in self.color)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)
    
    def is_alive(self) -> bool:
        """Check if particle is still active"""
        return self.lifetime > 0

class ParticleEffects:
    """Manages all particle effects"""
    
    def __init__(self):
        self.particles: List[Particle] = []
    
    def blood_splash(self, x: float, y: float, count: int = 10):
        """Create blood splash effect"""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 3)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            particle = Particle(x, y, vx, vy, (200, 0, 0), 30, 3)
            self.particles.append(particle)
    
    def dust_cloud(self, x: float, y: float, count: int = 8):
        """Create dust effect"""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.5, 1.5)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 0.5
            particle = Particle(x, y, vx, vy, (150, 150, 100), 40, 2)
            self.particles.append(particle)
    
    def water_splash(self, x: float, y: float, count: int = 12):
        """Create water splash effect"""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.5, 2)
            vx = math.cos(angle) * speed
            vy = (math.sin(angle) * speed) - 1
            particle = Particle(x, y, vx, vy, (100, 150, 200), 25, 2)
            self.particles.append(particle)
    
    def rain_particles(self, screen_width: int, screen_height: int, intensity: float = 0.5):
        """Create rain effect"""
        count = int(intensity * 50)
        for _ in range(count):
            x = random.uniform(0, screen_width)
            y = random.uniform(0, screen_height)
            particle = Particle(x, y, 0, 2, (150, 150, 200), 60, 1)
            self.particles.append(particle)
    
    def snow_particles(self, screen_width: int, screen_height: int, intensity: float = 0.3):
        """Create snow effect"""
        count = int(intensity * 30)
        for _ in range(count):
            x = random.uniform(0, screen_width)
            y = random.uniform(0, screen_height)
            vx = random.uniform(-0.5, 0.5)
            particle = Particle(x, y, vx, 0.5, (220, 220, 255), 80, 2)
            self.particles.append(particle)
    
    def update(self):
        """Update all particles"""
        for particle in self.particles:
            particle.update()
        
        self.particles = [p for p in self.particles if p.is_alive()]
    
    def draw(self, surface: pygame.Surface):
        """Draw all particles"""
        for particle in self.particles:
            particle.draw(surface)
    
    def clear(self):
        """Clear all particles"""
        self.particles.clear()
