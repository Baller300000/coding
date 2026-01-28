"""Disease and health system"""

import random
from typing import List, TYPE_CHECKING
from ..utils.constants import (
    DISEASE_SPREAD_RADIUS, DISEASE_INFECTION_CHANCE, 
    DISEASE_DEATH_CHANCE, DISEASE_RECOVERY_TIME
)

if TYPE_CHECKING:
    from ..core.animal import Animal

class Disease:
    """Represents a disease affecting animals"""
    
    def __init__(self, name: str = "illness"):
        self.name = name
        self.severity = random.uniform(0.5, 1.0)
        self.infected_animals: set = set()
    
    def infect(self, animal: 'Animal'):
        """Infect an animal"""
        if not hasattr(animal, 'health'):
            animal.health = 100
        if not hasattr(animal, 'disease'):
            animal.disease = None
            animal.disease_timer = 0
            animal.disease_severity = 0
        
        animal.disease = self
        animal.disease_timer = DISEASE_RECOVERY_TIME
        animal.disease_severity = self.severity
        self.infected_animals.add(id(animal))
    
    def spread(self, animals: List['Animal']):
        """Spread disease among nearby animals"""
        for animal in animals:
            if id(animal) in self.infected_animals:
                for other in animals:
                    if (id(other) not in self.infected_animals and
                        animal.position.distance_to(other.position) < DISEASE_SPREAD_RADIUS):
                        if random.random() < DISEASE_INFECTION_CHANCE:
                            self.infect(other)
    
    def update_animal(self, animal: 'Animal') -> bool:
        """Update animal disease state. Returns True if died"""
        if id(animal) not in self.infected_animals:
            return False
        
        animal.disease_timer -= 1
        
        # Reduce energy from disease
        animal.energy -= animal.energy * animal.disease_severity * 0.01
        
        # Check death
        if random.random() < DISEASE_DEATH_CHANCE * animal.disease_severity:
            return True
        
        # Check recovery
        if animal.disease_timer <= 0:
            animal.disease = None
            animal.disease_severity = 0
            self.infected_animals.discard(id(animal))
        
        return False

class HealthSystem:
    """Manages animal health and diseases"""
    
    def __init__(self):
        self.active_diseases: List[Disease] = []
    
    def create_outbreak(self, animals: List['Animal'], patient_zero: 'Animal'):
        """Create a disease outbreak"""
        disease = Disease("outbreak")
        disease.infect(patient_zero)
        self.active_diseases.append(disease)
    
    def update(self, animals: List['Animal']):
        """Update all diseases"""
        dead_animals = []
        
        for disease in self.active_diseases:
            disease.spread(animals)
            for animal in animals:
                if disease.update_animal(animal):
                    dead_animals.append(animal)
        
        return dead_animals
