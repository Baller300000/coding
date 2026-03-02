# Window settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

# Planet settings - reduced for performance
CHUNK_SIZE = 16
WORLD_HEIGHT = 16
TERRAIN_SCALE = 0.1
RENDER_DISTANCE = 80  # Only render blocks within this distance
SURFACE_ONLY = True  # Only render surface blocks

# Block types
class BlockType:
    AIR = 0
    GRASS = 1
    DIRT = 2
    STONE = 3
    SAND = 4
    WATER = 5
    WOOD = 6
    LEAVES = 7

# Block colors (RGB)
BLOCK_COLORS = {
    BlockType.AIR: (10, 10, 30),
    BlockType.GRASS: (34, 139, 34),
    BlockType.DIRT: (139, 69, 19),
    BlockType.STONE: (128, 128, 128),
    BlockType.SAND: (194, 178, 128),
    BlockType.WATER: (0, 119, 182),
    BlockType.WOOD: (101, 67, 33),
    BlockType.LEAVES: (0, 100, 0),
}

# Animal types
class AnimalTypes:
    HERBIVORE = "herbivore"
    CARNIVORE = "carnivore"
    BIRD = "bird"
    RABBIT = "rabbit"
    DEER = "deer"
    WOLF = "wolf"
    FISH = "fish"
    MOUSE = "mouse"
    FOX = "fox"
    EAGLE = "eagle"
    DUCK = "duck"
    TURTLE = "turtle"

# Animal colors and settings
ANIMAL_CONFIGS = {
    AnimalTypes.RABBIT: {"color": (200, 200, 200), "speed": 0.8, "energy": 100, "vision": 25},
    AnimalTypes.DEER: {"color": (139, 69, 19), "speed": 1.0, "energy": 150, "vision": 40},
    AnimalTypes.MOUSE: {"color": (100, 100, 100), "speed": 0.6, "energy": 50, "vision": 15},
    AnimalTypes.WOLF: {"color": (200, 50, 50), "speed": 1.2, "energy": 200, "vision": 50},
    AnimalTypes.FOX: {"color": (255, 165, 0), "speed": 1.1, "energy": 180, "vision": 45},
    AnimalTypes.BIRD: {"color": (255, 200, 0), "speed": 1.5, "energy": 60, "vision": 60},
    AnimalTypes.EAGLE: {"color": (139, 69, 19), "speed": 2.0, "energy": 120, "vision": 80},
    AnimalTypes.DUCK: {"color": (0, 100, 150), "speed": 1.3, "energy": 70, "vision": 35},
    AnimalTypes.FISH: {"color": (255, 100, 0), "speed": 0.9, "energy": 40, "vision": 20},
    AnimalTypes.TURTLE: {"color": (100, 100, 0), "speed": 0.4, "energy": 80, "vision": 20},
}

# Initial animal counts - reduced for performance
INITIAL_ANIMALS = {
    AnimalTypes.RABBIT: 4,
    AnimalTypes.DEER: 2,
    AnimalTypes.MOUSE: 3,
    AnimalTypes.BIRD: 3,
    AnimalTypes.EAGLE: 1,
    AnimalTypes.DUCK: 2,
    AnimalTypes.WOLF: 1,
    AnimalTypes.FOX: 1,
    AnimalTypes.FISH: 3,
    AnimalTypes.TURTLE: 2,
}

# Camera settings
DEFAULT_ZOOM = 1.2
CAMERA_DISTANCE = 300
CAMERA_SPEED = 1.5

# Breeding settings
BREEDING_ENERGY_THRESHOLD = 1.2
BREEDING_ENERGY_COST = 0.4
BREEDING_AGE_MIN = 120
BREEDING_COOLDOWN = 200

# Weather system
WEATHER_TYPES = ["clear", "rain", "snow"]
WEATHER_DURATION = 300  # frames
WEATHER_CHANGE_CHANCE = 0.01  # per frame
RAIN_EFFECT_INTENSITY = 0.8  # visibility reduction
SNOW_EFFECT_INTENSITY = 0.6  # visibility reduction

# Day/Night cycle
DAY_LENGTH = 2000  # frames (33 seconds at 60 FPS)
NIGHT_BRIGHTNESS = 0.3  # 0-1
DAY_BRIGHTNESS = 1.0

# Seasons
SEASON_DURATION = 4000  # frames per season
SEASONS = ["spring", "summer", "autumn", "winter"]
SEASON_COLORS = {
    "spring": (0.7, 1.0, 0.7),  # RGB multipliers
    "summer": (1.0, 1.0, 0.6),
    "autumn": (1.0, 0.8, 0.4),
    "winter": (0.8, 0.9, 1.0),
}

# Biome types
class Biome:
    GRASSLAND = "grassland"
    FOREST = "forest"
    DESERT = "desert"
    MOUNTAIN = "mountain"
    SWAMP = "swamp"

BIOME_TERRAINS = {
    Biome.GRASSLAND: {"grass": 0.8, "dirt": 0.2},
    Biome.FOREST: {"leaves": 0.6, "wood": 0.3, "grass": 0.1},
    Biome.DESERT: {"sand": 0.9, "stone": 0.1},
    Biome.MOUNTAIN: {"stone": 0.8, "dirt": 0.2},
    Biome.SWAMP: {"water": 0.5, "dirt": 0.5},
}

BIOME_ANIMALS = {
    Biome.GRASSLAND: [AnimalTypes.RABBIT, AnimalTypes.DEER, AnimalTypes.WOLF, AnimalTypes.EAGLE],
    Biome.FOREST: [AnimalTypes.DEER, AnimalTypes.MOUSE, AnimalTypes.BIRD, AnimalTypes.FOX],
    Biome.DESERT: [AnimalTypes.MOUSE, AnimalTypes.BIRD],
    Biome.MOUNTAIN: [AnimalTypes.EAGLE, AnimalTypes.FOX],
    Biome.SWAMP: [AnimalTypes.DUCK, AnimalTypes.FISH, AnimalTypes.TURTLE],
}

# Temperature system
BASE_TEMPERATURE = 20  # Celsius
SEASON_TEMPERATURE = {
    "spring": 15,
    "summer": 25,
    "autumn": 15,
    "winter": 5,
}
WEATHER_TEMPERATURE = {
    "clear": 0,
    "rain": -2,
    "snow": -5,
}

# Genetics
GENETIC_VARIATION = 0.2  # 20% variation in traits per generation
TRAIT_MUTATION_CHANCE = 0.1  # 10% chance of mutation

# Disease system
DISEASE_SPREAD_RADIUS = 15
DISEASE_INFECTION_CHANCE = 0.05  # per frame if near infected
DISEASE_DEATH_CHANCE = 0.02  # per frame if infected
DISEASE_RECOVERY_TIME = 500  # frames

# Starvation
STARVATION_DAMAGE = 0.1  # energy loss per frame when very hungry
CRITICAL_HUNGER_THRESHOLD = 0.2  # energy / max_energy

# Pack behavior
PACK_FORMATION_DISTANCE = 20
PACK_HUNT_BONUS = 1.5  # damage multiplier

# Migration
MIGRATION_DISTANCE = 30
MIGRATION_THRESHOLD_POPULATION = 10
MIGRATION_FOOD_THRESHOLD = 0.3  # food abundance

# Plant growth
PLANT_GROWTH_CHANCE = 0.05  # per frame per grass block
PLANT_MAX_AGE = 1000  # frames

# Nesting
NEST_CONSTRUCTION_FRAMES = 200
NEST_RETURN_DISTANCE = 10
