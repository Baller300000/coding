# Project Structure Documentation

## Filesystem Organization

graph```
generated-planet/
├── main.py                           # Entry point (imports from src.simulation)
├── src/                              # Main source package
│   ├── __init__.py                   # Package initialization with PlanetSimulation export
│   ├── simulation.py                 # Main orchestrator (PlanetSimulation class)
│   │
│   ├── core/                         # Core simulation logic
│   │   ├── __init__.py
│   │   ├── planet.py                 # Terrain generation (Planet class)
│   │   ├── animal.py                 # Animal entities (Animal class)
│   │   └── ecosystem.py              # World management (Ecosystem class)
│   │
│   ├── rendering/                    # Graphics and visualization
│   │   ├── __init__.py
│   │   ├── camera.py                 # 3D camera with projection (Camera class)
│   │   ├── renderer.py               # Main renderer (Renderer class)
│   │   └── sprites.py                # Sprite drawing functions
│   │
│   ├── engine/                       # Game logic and systems
│   │   ├── __init__.py
│   │   ├── behaviors.py              # Animal AI (BehaviorEngine, ReproductionEngine)
│   │   └── input_handler.py          # Input management (InputHandler class)
│   │
│   ├── ui/                           # User interface
│   │   ├── __init__.py
│   │   └── hud.py                    # HUD, Minimap, Stats classes
│   │
│   └── utils/                        # Shared utilities
│       ├── __init__.py
│       ├── constants.py              # Global configuration and constants
│       └── vectors.py                # Vector3 math class and functions
graph```

## Dependency Graph

================

main.py
  └─> src.simulation.PlanetSimulation
        ├─> src.rendering.camera.Camera
        │   └─> src.utils.vectors (Vector3, rotate_x, rotate_y)
        │   └─> src.utils.constants (WINDOW_WIDTH, WINDOW_HEIGHT, etc.)
        │
        ├─> src.rendering.renderer.Renderer
        │   ├─> src.rendering.camera.Camera
        │   ├─> src.rendering.sprites
        │   └─> src.utils.constants (BLOCK_COLORS, BlockType, etc.)
        │
        ├─> src.ui.hud (HUD, Minimap, Stats)
        │   └─> src.utils.constants (WINDOW_WIDTH, WINDOW_HEIGHT)
        │
        ├─> src.engine.input_handler.InputHandler
        │   └─> src.utils.constants (CAMERA_SPEED)
        │
        ├─> src.core.ecosystem.Ecosystem
        │   ├─> src.core.planet.Planet
        │   │   ├─> src.utils.vectors.Vector3
        │   │   └─> src.utils.constants (BlockType, WORLD_HEIGHT, CHUNK_SIZE, etc.)
        │   │
        │   ├─> src.core.animal.Animal
        │   │   ├─> src.utils.vectors.Vector3
        │   │   └─> src.utils.constants (AnimalTypes, ANIMAL_CONFIGS, BlockType, BREEDING_*)
        │   │
        │   └─> src.utils.constants (AnimalTypes, INITIAL_ANIMALS, BREEDING_*, BlockType)
        │
        └─> src.engine.behaviors (BehaviorEngine, ReproductionEngine)
            ├─> src.utils.vectors.Vector3
            └─> src.utils.constants (AnimalTypes, BlockType)

MODULE BREAKDOWN

1. src/utils/
   - constants.py: Window settings, terrain config, animal types/colors, breeding settings
   - vectors.py: Vector3 class with math operations, rotation functions

2. src/core/
   - planet.py: Terrain generation, chunk-based voxel world, block management
   - animal.py: Animal entity class with movement, eating, reproduction
   - ecosystem.py: Manages planet + animals, handles updates and initialization

3. src/rendering/
   - camera.py: 3D perspective projection, camera movement
   - renderer.py: Orchestrates terrain and animal rendering
   - sprites.py: Drawing functions for animals, blocks, UI elements

4. src/engine/
   - behaviors.py: Static AI engines for animal behavior and reproduction
   - input_handler.py: Keyboard event handling and camera control

5. src/ui/
   - hud.py: HUD info panel, species list, minimap, statistics

6. src/simulation.py
   - PlanetSimulation: Main class that ties all systems together

IMPORT STRUCTURE

All imports use relative paths from within the src package:

- From core modules: from ..utils.constants import ...
- From rendering modules: from ..utils.vectors import ...
- From engine modules: from ..core.ecosystem import ...
- Cross-package: TYPE_CHECKING for circular dependency prevention

HOW TO RUN

python main.py

The main.py at project root imports from src.simulation and starts the simulation.
All module dependencies are automatically resolved through relative imports.

BENEFITS OF THIS STRUCTURE

1. Separation of Concerns
   - Core simulation, rendering, UI, and engine logic are clearly separated
   - Easy to find and modify specific functionality

2. Scalability
   - New features (e.g., networking, advanced graphics) can be added as new packages
   - Existing code doesn't need modification

3. Maintainability
   - Clear folder structure mirrors the code architecture
   - Dependencies are explicit and manageable

4. Reusability
   - Core components (Animal, Planet, Ecosystem) can be used independently
   - Utilities (Vector3, constants) are available to all modules

5. Testing
   - Each module can be unit tested independently
   - Mock implementations are easier to provide

6. Professional Structure
   - Follows Python packaging best practices
   - Ready for distribution or team collaboration
