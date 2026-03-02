"""Behaviors module - animal behavior logic extracted from animal class"""

from typing import List, Optional, TYPE_CHECKING
import random
import math
from ..utils.vectors import Vector3
from ..utils.constants import AnimalTypes, BlockType

if TYPE_CHECKING:
    from ..core.planet import Planet
    from ..core.animal import Animal

class BehaviorEngine:
    """Handles all animal behavior logic"""
    
    @staticmethod
    def find_target(animal: 'Animal', planet: 'Planet', animals: List['Animal']) -> Optional[Vector3]:
        """Find food or prey"""
        best_target = None
        best_distance = float('inf')
        
        if animal.is_herbivore:
            # Look for grass/leaves nearby
            nearby = planet.get_nearby_blocks(animal.position, animal.vision_range)
            for (x, y, z), block_type in nearby:
                if block_type in [BlockType.GRASS, BlockType.LEAVES]:
                    target_pos = Vector3(x, y, z)
                    distance = animal.position.distance_to(target_pos)
                    if distance < best_distance:
                        best_distance = distance
                        best_target = target_pos
        
        elif animal.is_carnivore or animal.is_water:
            # Look for prey
            prey_types = []
            if animal.is_carnivore:
                prey_types = [AnimalTypes.RABBIT, AnimalTypes.MOUSE, AnimalTypes.DUCK]
                if animal.animal_type == AnimalTypes.EAGLE:
                    prey_types += [AnimalTypes.BIRD]
            else:  # Water animals
                prey_types = [AnimalTypes.FISH, AnimalTypes.DUCK]
            
            for target_animal in animals:
                if target_animal.animal_type in prey_types:
                    distance = animal.position.distance_to(target_animal.position)
                    if distance < animal.vision_range and distance < best_distance:
                        best_distance = distance
                        best_target = target_animal.position
        
        return best_target
    
    @staticmethod
    def move_towards(animal: 'Animal', target: Vector3):
        """Move animal towards target"""
        direction = (target - animal.position).normalize()
        animal.position = animal.position + direction * animal.speed
    
    @staticmethod
    def random_walk(animal: 'Animal'):
        """Random movement"""
        direction = Vector3(
            random.uniform(-1, 1),
            random.uniform(-0.3, 0.3) if not animal.is_bird else random.uniform(-0.5, 0.5),
            random.uniform(-1, 1)
        ).normalize()
        animal.position = animal.position + direction * animal.speed
        
        # Bound checking
        animal.position.x = max(-50, min(50, animal.position.x))
        animal.position.y = max(0, min(20, animal.position.y))
        animal.position.z = max(-50, min(50, animal.position.z))
    
    @staticmethod
    def eat(animal: 'Animal', planet: 'Planet', animals: List['Animal'], target: Vector3):
        """Animal eats food or prey"""
        if animal.is_herbivore:
            x, y, z = int(target.x), int(target.y), int(target.z)
            block = planet.get_block_at(x, y, z)
            if block in [BlockType.GRASS, BlockType.LEAVES]:
                planet.set_block_at(x, y, z, BlockType.DIRT if block == BlockType.GRASS else BlockType.AIR)
                animal.energy += 25
        else:
            for other_animal in animals[:]:
                if animal.position.distance_to(other_animal.position) < 2:
                    animal.energy += other_animal.max_energy
                    animals.remove(other_animal)
                    break
    
    @staticmethod
    def constrain_to_ground(animal: 'Animal', planet: 'Planet'):
        """Keep animals on ground or in water"""
        x, z = int(animal.position.x), int(animal.position.z)
        
        if animal.is_water:
            # Find water level
            for y in range(15, -1, -1):
                if planet.get_block_at(x, y, z) == BlockType.WATER:
                    animal.position.y = y + 1
                    return
            # If no water, fall to ground
            animal.is_water = False
        
        # Find ground level
        for y in range(15, -1, -1):
            block = planet.get_block_at(x, y, z)
            if block != BlockType.AIR and block != BlockType.WATER:
                animal.position.y = y + 1
                return
        
        animal.position.y = 1

class ReproductionEngine:
    """Handles breeding logic"""
    
    @staticmethod
    def can_breed(animal: 'Animal', breeding_energy_threshold: float, breeding_age_min: int, 
                 breeding_cooldown: int) -> bool:
        """Check if animal can breed"""
        return (animal.energy > animal.max_energy * breeding_energy_threshold and 
                animal.age > breeding_age_min and 
                animal.breeding_cooldown == 0)
    
    @staticmethod
    def breed(animal: 'Animal', breeding_energy_cost: float, breeding_cooldown: int):
        """Execute breeding"""
        animal.energy -= animal.max_energy * breeding_energy_cost
        animal.breeding_cooldown = breeding_cooldown
        animal.is_breeding = True
        return animal.reproduce()
