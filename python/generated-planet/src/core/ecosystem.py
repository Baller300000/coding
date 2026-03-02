"""Ecosystem module - world management and ecosystem simulation"""

import random
import math
from typing import List
from ..utils.vectors import Vector3
from .planet import Planet
from .animal import Animal
from .health import HealthSystem
from ..engine.weather import WeatherSystem
from ..utils.constants import (
    AnimalTypes, INITIAL_ANIMALS, BREEDING_ENERGY_THRESHOLD, 
    BREEDING_ENERGY_COST, BREEDING_AGE_MIN, BREEDING_COOLDOWN, BlockType,
    PLANT_GROWTH_CHANCE, PLANT_MAX_AGE
)

class Ecosystem:
    """Manages the ecosystem - animals, food, breeding"""
    
    def __init__(self):
        self.planet = Planet()
        self.animals: List[Animal] = []
        self.frame_count = 0
        self.health_system = HealthSystem()
        self.weather = WeatherSystem()
        self.plant_ages = {}  # Track plant growth
        self.add_water_lake()
        self.initialize_animals()
    
    def add_water_lake(self):
        """Add water blocks in the center"""
        for x in range(-10, 11):
            for z in range(-10, 11):
                dist = math.sqrt(x**2 + z**2)
                if dist < 8:
                    for y in range(0, 4):
                        self.planet.blocks[(x, y, z)] = BlockType.WATER
                        self.planet.surface_blocks.add((x, y, z))
    
    def initialize_animals(self):
        """Spawn initial animals"""
        spawn_height = 10
        for animal_type, count in INITIAL_ANIMALS.items():
            for _ in range(count):
                pos = Vector3(
                    random.uniform(-25, 25),
                    spawn_height,
                    random.uniform(-25, 25)
                )
                self.animals.append(Animal(animal_type, pos))
    
    def get_animal_counts(self) -> dict:
        """Get count of each animal type"""
        counts = {}
        for animal in self.animals:
            counts[animal.animal_type] = counts.get(animal.animal_type, 0) + 1
        return counts
    
    def get_breeding_count(self) -> int:
        """Count animals currently breeding"""
        return sum(1 for a in self.animals if a.is_breeding)
    
    def update(self, behavior_engine, reproduction_engine):
        """Update ecosystem"""
        self.frame_count += 1
        
        # Update weather and environmental systems
        self.weather.update()
        
        # Update planet
        if self.frame_count % 60 == 0:
            self.planet.update()
        
        # Plant growth
        self.update_plant_growth()
        
        # Update animals
        new_animals = []
        dead_from_disease = []
        
        for animal in self.animals:
            # Update basic state
            animal.age += 1
            animal.energy -= animal.speed * 0.2
            animal.breeding_cooldown = max(0, animal.breeding_cooldown - 1)
            
            # Keep on ground
            behavior_engine.constrain_to_ground(animal, self.planet)
            
            # Find and pursue target
            target = behavior_engine.find_target(animal, self.planet, self.animals)
            if target:
                behavior_engine.move_towards(animal, target)
                behavior_engine.eat(animal, self.planet, self.animals, target)
            else:
                behavior_engine.random_walk(animal)
            
            # Try to breed
            if reproduction_engine.can_breed(animal, BREEDING_ENERGY_THRESHOLD, 
                                            BREEDING_AGE_MIN, BREEDING_COOLDOWN):
                offspring = reproduction_engine.breed(animal, BREEDING_ENERGY_COST, BREEDING_COOLDOWN)
                new_animals.append(offspring)
            else:
                animal.is_breeding = False
        
        self.animals.extend(new_animals)
        
        # Handle diseases
        disease_deaths = self.health_system.update(self.animals)
        dead_from_disease.extend(disease_deaths)
        
        # Remove dead animals
        for dead in dead_from_disease:
            if dead in self.animals:
                self.animals.remove(dead)
        
        self.animals = [a for a in self.animals if a.is_alive()]
        
        # Generate terrain around animals
        if self.frame_count % 30 == 0:
            for animal in self.animals:
                chunk_x = int(animal.position.x / 16) * 16
                chunk_z = int(animal.position.z / 16) * 16
                self.planet.generate_chunk(chunk_x, chunk_z)
    
    def update_plant_growth(self):
        """Update plant growth on grass blocks"""
        if self.frame_count % 10 != 0:
            return
        
        # Grow some grass
        for _ in range(5):
            x = random.randint(-32, 32)
            z = random.randint(-32, 32)
            for y in range(1, 16):
                if self.planet.get_block_at(x, y, z) == BlockType.DIRT:
                    if y < 15 and self.planet.get_block_at(x, y+1, z) == BlockType.AIR:
                        if random.random() < PLANT_GROWTH_CHANCE:
                            self.planet.set_block_at(x, y+1, z, BlockType.GRASS)
    
    def get_total_animals(self) -> int:
        """Total animal count"""
        return len(self.animals)
    
    def get_time_seconds(self) -> int:
        """Get elapsed time in seconds"""
        return self.frame_count // 60
