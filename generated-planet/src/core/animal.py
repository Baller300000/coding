from enum import Enum
from typing import List, Optional, TYPE_CHECKING
import random
import math
from ..utils.vectors import Vector3
from ..utils.constants import (
    AnimalTypes, ANIMAL_CONFIGS, BlockType, 
    BREEDING_ENERGY_THRESHOLD, BREEDING_ENERGY_COST, BREEDING_AGE_MIN, BREEDING_COOLDOWN,
    STARVATION_DAMAGE, CRITICAL_HUNGER_THRESHOLD, CRITICAL_HUNGER_THRESHOLD,
    NEST_CONSTRUCTION_FRAMES, NEST_RETURN_DISTANCE, MIGRATION_DISTANCE
)
from .genetics import Genetics

if TYPE_CHECKING:
    from .planet import Planet

class Animal:
    """Base animal class with advanced features"""
    
    def __init__(self, animal_type: str, position: Vector3, parent=None):
        self.animal_type = animal_type
        self.position = position
        self.age = 0
        self.breeding_cooldown = 0
        self.is_breeding = False
        
        config = ANIMAL_CONFIGS.get(animal_type, {})
        base_speed = config.get("speed", 0.5)
        base_color = config.get("color", (100, 100, 100))
        base_vision = config.get("vision", 30)
        self.max_energy = config.get("energy", 100)
        
        # Genetics system
        self.genetics = Genetics(base_speed, base_color, base_vision, 
                                 parent.genetics if parent else None)
        self.speed = self.genetics.speed
        self.color = self.genetics.color
        self.vision_range = self.genetics.vision
        
        # Start with reduced energy if offspring
        if parent:
            self.energy = self.max_energy * 0.7
        else:
            self.energy = self.max_energy
        
        # Type classification
        self.is_herbivore = animal_type in [AnimalTypes.RABBIT, AnimalTypes.DEER, AnimalTypes.MOUSE, AnimalTypes.DUCK, AnimalTypes.TURTLE]
        self.is_carnivore = animal_type in [AnimalTypes.WOLF, AnimalTypes.FOX, AnimalTypes.EAGLE]
        self.is_bird = animal_type in [AnimalTypes.BIRD, AnimalTypes.EAGLE, AnimalTypes.DUCK]
        self.is_water = animal_type in [AnimalTypes.FISH, AnimalTypes.TURTLE, AnimalTypes.DUCK]
        
        # New systems
        self.pack = None
        self.disease = None
        self.disease_timer = 0
        self.disease_severity = 0
        self.nest_position = None
        self.nest_construction = 0
        self.home_range = position.copy() if hasattr(position, 'copy') else position
        self.aggression = 0.2
        self.hunger_level = 0  # 0-1, 0 = full, 1 = starving
    
    def update(self, planet: 'Planet', animals: List['Animal']) -> Optional['Animal']:
        """Update animal state"""
        self.age += 1
        
        # Update hunger (starvation mechanic)
        self.hunger_level = max(0, min(1, (1 - self.energy / self.max_energy)))
        
        # Starvation damage
        if self.hunger_level > CRITICAL_HUNGER_THRESHOLD:
            self.energy -= STARVATION_DAMAGE * self.energy
        
        self.energy -= self.speed * 0.2
        self.breeding_cooldown = max(0, self.breeding_cooldown - 1)
        
        # Keep animals on ground or in water
        self.constrain_position(planet)
        
        target = self.find_target(planet, animals)
        
        if target:
            self.move_towards(target)
            self.eat(planet, animals, target)
        else:
            self.random_walk()
        
        # Reproduce when conditions are met
        if self.energy > self.max_energy * BREEDING_ENERGY_THRESHOLD and self.age > BREEDING_AGE_MIN and self.breeding_cooldown == 0:
            self.energy -= self.max_energy * BREEDING_ENERGY_COST
            self.breeding_cooldown = BREEDING_COOLDOWN
            self.is_breeding = True
            return self.reproduce()
        
        self.is_breeding = False
        return None
    
    def constrain_position(self, planet: 'Planet'):
        """Keep animals on ground or in water"""
        x, z = int(self.position.x), int(self.position.z)
        
        if self.is_water:
            # Find water level
            for y in range(15, -1, -1):
                if planet.get_block_at(x, y, z) == BlockType.WATER:
                    self.position.y = y + 1
                    return
            # If no water, fall to ground
            self.is_water = False
        
        # Find ground level
        for y in range(15, -1, -1):
            block = planet.get_block_at(x, y, z)
            if block != BlockType.AIR and block != BlockType.WATER:
                self.position.y = y + 1
                return
        
        self.position.y = 1
    
    def find_target(self, planet: 'Planet', animals: List['Animal']) -> Optional[Vector3]:
        """Find food or prey"""
        best_target = None
        best_distance = float('inf')
        
        if self.is_herbivore:
            # Look for grass/leaves nearby
            nearby = planet.get_nearby_blocks(self.position, self.vision_range)
            for (x, y, z), block_type in nearby:
                if block_type in [BlockType.GRASS, BlockType.LEAVES]:
                    target_pos = Vector3(x, y, z)
                    distance = self.position.distance_to(target_pos)
                    if distance < best_distance:
                        best_distance = distance
                        best_target = target_pos
        
        elif self.is_carnivore or self.is_water:
            # Look for prey
            prey_types = []
            if self.is_carnivore:
                prey_types = [AnimalTypes.RABBIT, AnimalTypes.MOUSE, AnimalTypes.DUCK]
                if self.animal_type == AnimalTypes.EAGLE:
                    prey_types += [AnimalTypes.BIRD]
            else:  # Water animals
                prey_types = [AnimalTypes.FISH, AnimalTypes.DUCK]
            
            for animal in animals:
                if animal.animal_type in prey_types:
                    distance = self.position.distance_to(animal.position)
                    if distance < self.vision_range and distance < best_distance:
                        best_distance = distance
                        best_target = animal.position
        
        return best_target
    
    def move_towards(self, target: Vector3):
        """Move towards target"""
        direction = (target - self.position).normalize()
        self.position = self.position + direction * self.speed
    
    def random_walk(self):
        """Move randomly"""
        direction = Vector3(
            random.uniform(-1, 1),
            random.uniform(-0.3, 0.3) if not self.is_bird else random.uniform(-0.5, 0.5),
            random.uniform(-1, 1)
        ).normalize()
        self.position = self.position + direction * self.speed
        
        # Bound checking
        self.position.x = max(-50, min(50, self.position.x))
        self.position.y = max(0, min(20, self.position.y))
        self.position.z = max(-50, min(50, self.position.z))
    
    def eat(self, planet: 'Planet', animals: List['Animal'], target: Vector3):
        """Eat food or prey"""
        if self.is_herbivore:
            x, y, z = int(target.x), int(target.y), int(target.z)
            block = planet.get_block_at(x, y, z)
            if block in [BlockType.GRASS, BlockType.LEAVES]:
                planet.set_block_at(x, y, z, BlockType.DIRT if block == BlockType.GRASS else BlockType.AIR)
                self.energy += 25
        else:
            for animal in animals[:]:
                if self.position.distance_to(animal.position) < 2:
                    self.energy += animal.max_energy
                    animals.remove(animal)
                    break
    
    def reproduce(self) -> 'Animal':
        """Create offspring"""
        offset = Vector3(
            random.uniform(-5, 5),
            0,
            random.uniform(-5, 5)
        )
        offspring = Animal(self.animal_type, self.position + offset, parent=self)
        # Inherit some traits from parent
        offspring.genetics = Genetics(self.genetics.speed, self.genetics.color, 
                                     self.genetics.vision, self.genetics)
        return offspring
    
    def is_alive(self) -> bool:
        """Check if still alive"""
        return self.energy > 0 and self.age < 3000
