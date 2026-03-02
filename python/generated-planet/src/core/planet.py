import random
import math
from typing import Dict, Tuple, Set, List
from ..utils.vectors import Vector3
from ..utils.constants import BlockType, WORLD_HEIGHT, CHUNK_SIZE, RENDER_DISTANCE

class Planet:
    """3D Minecraft-style voxel terrain planet - optimized"""
    
    def __init__(self, seed: int = 42):
        self.seed = seed
        random.seed(seed)
        self.blocks: Dict[Tuple[int, int, int], int] = {}
        self.surface_blocks: Set[Tuple[int, int, int]] = set()
        self.chunks_generated = set()
        self.generate_initial_terrain()
    
    def generate_initial_terrain(self):
        """Generate initial terrain around spawn area - smaller"""
        for x in range(-32, 33, CHUNK_SIZE):
            for z in range(-32, 33, CHUNK_SIZE):
                self.generate_chunk(x, z)
    
    def generate_chunk(self, chunk_x: int, chunk_z: int):
        """Generate a chunk of terrain"""
        chunk_key = (chunk_x // CHUNK_SIZE, chunk_z // CHUNK_SIZE)
        if chunk_key in self.chunks_generated:
            return
        
        self.chunks_generated.add(chunk_key)
        
        for x in range(chunk_x, chunk_x + CHUNK_SIZE):
            for z in range(chunk_z, chunk_z + CHUNK_SIZE):
                height = self.get_terrain_height(x, z)
                
                for y in range(0, int(height) + 1):
                    block_type = self.get_block_type(x, y, z, height)
                    if block_type != BlockType.AIR:
                        self.blocks[(x, y, z)] = block_type
                        if y == int(height):
                            self.surface_blocks.add((x, y, z))
                
                # Add trees on grass
                if int(height) > 3 and random.random() < 0.08:
                    self.place_tree(x, int(height) + 1, z)
    
    def place_tree(self, x: int, y: int, z: int):
        """Place a tree at coordinates"""
        height = random.randint(3, 5)
        
        for i in range(height):
            self.blocks[(x, y + i, z)] = BlockType.WOOD
            self.surface_blocks.add((x, y + i, z))
        
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                for dy in range(height - 2, height + 1):
                    pos = (x + dx, y + dy, z + dz)
                    if pos not in self.blocks:
                        self.blocks[pos] = BlockType.LEAVES
                        self.surface_blocks.add(pos)
    
    def get_terrain_height(self, x: int, z: int) -> float:
        """Generate height at coordinates"""
        height = 0
        scale = 1.0
        amplitude = 1.0
        
        for octave in range(3):
            frequency = scale * 0.05
            value = math.sin(x * frequency) * math.cos(z * frequency)
            height += value * amplitude
            scale *= 2
            amplitude *= 0.5
        
        height = (height + 1.5) / 3.0
        height = 4 + height * 8
        return min(height, WORLD_HEIGHT - 1)
    
    def get_block_type(self, x: int, y: int, z: int, height: float) -> int:
        """Determine block type at coordinates"""
        if y > height:
            return BlockType.AIR
        
        if y < 0:
            return BlockType.STONE
        
        surface_y = int(height)
        
        if y == surface_y:
            if surface_y < 4:
                return BlockType.SAND
            return BlockType.GRASS
        
        if y > surface_y - 3:
            if surface_y < 4:
                return BlockType.SAND
            return BlockType.DIRT
        
        return BlockType.STONE
    
    def get_block_at(self, x: int, y: int, z: int) -> int:
        """Get block type at coordinates"""
        if y < 0 or y >= WORLD_HEIGHT:
            return BlockType.AIR
        
        chunk_x = (x // CHUNK_SIZE) * CHUNK_SIZE
        chunk_z = (z // CHUNK_SIZE) * CHUNK_SIZE
        self.generate_chunk(chunk_x, chunk_z)
        
        key = (x, y, z)
        return self.blocks.get(key, BlockType.AIR)
    
    def set_block_at(self, x: int, y: int, z: int, block_type: int):
        """Set block type at coordinates"""
        if 0 <= y < WORLD_HEIGHT:
            self.blocks[(x, y, z)] = block_type
            if block_type != BlockType.AIR:
                self.surface_blocks.add((x, y, z))
    
    def update(self):
        """Update planet state"""
        keys_to_update = []
        for (x, y, z), block_type in list(self.blocks.items())[:30]:
            if block_type == BlockType.DIRT and random.random() < 0.05:
                if y == int(self.get_terrain_height(x, z)):
                    keys_to_update.append(((x, y, z), BlockType.GRASS))
        
        for key, block_type in keys_to_update:
            self.blocks[key] = block_type
    
    def get_visible_blocks(self, camera_pos: Vector3) -> List[Tuple]:
        """Get only surface blocks within render distance"""
        visible = []
        for (x, y, z) in self.surface_blocks:
            block_pos = Vector3(x, y, z)
            distance = camera_pos.distance_to(block_pos)
            if distance < RENDER_DISTANCE:
                visible.append((x, y, z, self.blocks[(x, y, z)]))
        return visible
    
    def get_nearby_blocks(self, pos: Vector3, radius: float) -> List[Tuple]:
        """Get blocks near a position - for animal pathfinding"""
        nearby = []
        for (x, y, z), block_type in list(self.blocks.items())[:100]:
            block_pos = Vector3(x, y, z)
            if block_pos.distance_to(pos) < radius:
                nearby.append(((x, y, z), block_type))
        return nearby
