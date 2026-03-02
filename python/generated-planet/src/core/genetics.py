"""Genetic system for inherited traits"""

import random
from ..utils.constants import GENETIC_VARIATION, TRAIT_MUTATION_CHANCE

class Genetics:
    """Manages genetic traits for animals"""
    
    def __init__(self, speed: float = 1.0, color: tuple = (100, 100, 100), 
                 vision: float = 30, parent_genetics=None):
        """Initialize genetics, optionally inheriting from parent"""
        if parent_genetics:
            # Inherit from parent with variation
            self.speed = parent_genetics.speed * random.uniform(1 - GENETIC_VARIATION, 1 + GENETIC_VARIATION)
            self.color = self._mutate_color(parent_genetics.color)
            self.vision = parent_genetics.vision * random.uniform(1 - GENETIC_VARIATION, 1 + GENETIC_VARIATION)
            self.stamina = parent_genetics.stamina * random.uniform(1 - GENETIC_VARIATION, 1 + GENETIC_VARIATION)
            self.intelligence = parent_genetics.intelligence * random.uniform(1 - GENETIC_VARIATION, 1 + GENETIC_VARIATION)
        else:
            # Base traits
            self.speed = speed
            self.color = color
            self.vision = vision
            self.stamina = random.uniform(0.8, 1.2)
            self.intelligence = random.uniform(0.8, 1.2)
        
        # Clamp values
        self.speed = max(0.3, min(2.0, self.speed))
        self.vision = max(10, min(100, self.vision))
        self.stamina = max(0.3, min(2.0, self.stamina))
        self.intelligence = max(0.5, min(2.0, self.intelligence))
    
    def _mutate_color(self, base_color: tuple) -> tuple:
        """Mutate color with small random changes"""
        if random.random() < TRAIT_MUTATION_CHANCE:
            return (
                max(0, min(255, int(base_color[0] + random.randint(-20, 20)))),
                max(0, min(255, int(base_color[1] + random.randint(-20, 20)))),
                max(0, min(255, int(base_color[2] + random.randint(-20, 20)))),
            )
        return base_color
    
    def get_fitness(self) -> float:
        """Calculate overall fitness from traits"""
        return (self.speed + self.stamina + self.intelligence + (self.vision / 30)) / 4
