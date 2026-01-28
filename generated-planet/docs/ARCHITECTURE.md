"""
FILESYSTEM HIERARCHY - Generated Planet Simulation
===================================================

generated-planet/
│
├── README.md                         # Main project documentation
├── PROJECT_STRUCTURE.md              # Detailed structure documentation
│
├── main.py                           # Entry point - runs: python main.py
│   │
│   └─> imports from src/simulation.py
│
└── src/                              # Main source package
    │
    ├── __init__.py                   # Exports: PlanetSimulation
    ├── simulation.py                 # Main orchestrator (241 lines)
    │
    ├── core/                         # CORE SIMULATION LOGIC
    │   ├── __init__.py
    │   ├── planet.py                 # Terrain generation (156 lines)
    │   │   └─> Depends on: Vector3, BlockType, WORLD_HEIGHT, CHUNK_SIZE
    │   │
    │   ├── animal.py                 # Animal entities (153 lines)
    │   │   └─> Depends on: Vector3, AnimalTypes, ANIMAL_CONFIGS, BlockType
    │   │
    │   └── ecosystem.py              # World management (111 lines)
    │       └─> Depends on: Planet, Animal, INITIAL_ANIMALS, BlockType
    │
    ├── rendering/                    # GRAPHICS & VISUALIZATION
    │   ├── __init__.py
    │   │
    │   ├── camera.py                 # 3D camera (62 lines)
    │   │   ├─> project_3d_to_2d()
    │   │   ├─> move_forward/backward/left/right/up/down()
    │   │   ├─> rotate_yaw/pitch()
    │   │   └─> zoom_in/out()
    │   │
    │   ├── renderer.py               # Main renderer (62 lines)
    │   │   ├─> render_terrain()
    │   │   ├─> render_animals()
    │   │   └─> render_scene()
    │   │
    │   └── sprites.py                # Sprite drawing (73 lines)
    │       ├─> draw_3d_animal_sprite()
    │       ├─> draw_energy_bar()
    │       ├─> draw_breeding_indicator()
    │       └─> draw_terrain_block()
    │
    ├── engine/                       # GAME LOGIC & SYSTEMS
    │   ├── __init__.py
    │   │
    │   ├── behaviors.py              # Animal AI (99 lines)
    │   │   ├─> BehaviorEngine
    │   │   │   ├─> find_target()
    │   │   │   ├─> move_towards()
    │   │   │   ├─> random_walk()
    │   │   │   ├─> eat()
    │   │   │   └─> constrain_to_ground()
    │   │   │
    │   │   └─> ReproductionEngine
    │   │       ├─> can_breed()
    │   │       └─> breed()
    │   │
    │   └── input_handler.py          # Input management (48 lines)
    │       ├─> handle_events()
    │       ├─> update_camera()
    │       └─> is_key_pressed()
    │
    ├── ui/                           # USER INTERFACE
    │   ├── __init__.py
    │   │
    │   └── hud.py                    # UI components (115 lines)
    │       ├─> HUD class
    │       │   ├─> draw_info()
    │       │   ├─> draw_species_list()
    │       │   └─> draw_controls()
    │       │
    │       ├─> Minimap class
    │       │   └─> draw()
    │       │
    │       └─> Stats class
    │           ├─> update()
    │           └─> draw_summary()
    │
    └── utils/                        # SHARED UTILITIES
        ├── __init__.py
        │
        ├── constants.py              # Configuration (96 lines)
        │   ├─> Window settings (WINDOW_WIDTH/HEIGHT, FPS)
        │   ├─> Terrain (CHUNK_SIZE, WORLD_HEIGHT, RENDER_DISTANCE)
        │   ├─> BlockType enum
        │   ├─> AnimalTypes enum
        │   ├─> ANIMAL_CONFIGS dict
        │   ├─> INITIAL_ANIMALS dict
        │   ├─> BLOCK_COLORS dict
        │   └─> Breeding settings
        │
        └── vectors.py                # Vector math (58 lines)
            ├─> Vector3 dataclass
            │   ├─> Basic ops: +, -, *, distance_to()
            │   └─> normalize()
            │
            └─> Rotation functions
                ├─> rotate_x()
                ├─> rotate_y()
                └─> rotate_z()

MODULE STATISTICS
=================

Total Lines of Code: ~1,100+

Core Modules:

- planet.py:           156 lines
- animal.py:           153 lines
- ecosystem.py:        111 lines
Subtotal:              420 lines

Rendering Modules:

- camera.py:            62 lines
- renderer.py:          62 lines
- sprites.py:           73 lines
Subtotal:              197 lines

Engine Modules:

- behaviors.py:         99 lines
- input_handler.py:     48 lines
Subtotal:              147 lines

UI Modules:

- hud.py:              115 lines
Subtotal:              115 lines

Utilities:

- constants.py:         96 lines
- vectors.py:           58 lines
Subtotal:              154 lines

Orchestrator:

- simulation.py:       241 lines

Entry Point:

- main.py:               9 lines

DATA FLOW
=========

PlanetSimulation (main orchestrator)
│
├─ PlanetSimulation.run() <- main.py entry
│  │
│  ├─ handle_input() -> InputHandler.handle_events()
│  │  └─> Updates camera position/rotation
│  │
│  ├─ update()
│  │  └─> Ecosystem.update()
│  │     ├─> Planet.update()
│  │     ├─> BehaviorEngine.find_target() - for each animal
│  │     ├─> BehaviorEngine.move_towards() or random_walk()
│  │     ├─> BehaviorEngine.eat()
│  │     ├─> ReproductionEngine.breed() - if conditions met
│  │     └─> Remove dead animals
│  │
│  └─ draw()
│     ├─> Renderer.render_scene()
│     │  ├─> Camera.project_3d_to_2d() - for each block
│     │  ├─> draw_terrain_block() - visible blocks
│     │  ├─> Camera.project_3d_to_2d() - for each animal
│     │  └─> draw_3d_animal_sprite() - with energy bar, breeding indicator
│     │
│     └─> HUD.draw_*() - UI elements
│        ├─> draw_info() - FPS, time, counts
│        ├─> draw_species_list() - animal populations
│        ├─> draw_controls() - help text
│        └─> Minimap.draw() - overview

DEPENDENCY CHAINS
=================

Longest dependency chain (deepest import):
main.py
  -> src.simulation
    -> src.rendering.camera
      -> src.utils.vectors
      -> src.utils.constants

Most dependencies to single module:
src.utils.constants
  <- src.core.planet
  <- src.core.animal
  <- src.core.ecosystem
  <- src.rendering.camera
  <- src.rendering.renderer
  <- src.ui.hud
  <- src.engine.behaviors
  <- src.engine.input_handler
  <- src.simulation

DESIGN PATTERNS USED
====================

1. Module Organization Pattern
   - Logical separation by concern
   - Clear boundaries between systems
   - Relative imports for package coherence

2. Static Method Pattern (BehaviorEngine, ReproductionEngine)
   - Stateless utility classes
   - No instantiation overhead
   - Easy to test and reuse

3. Configuration Pattern (constants.py)
   - Centralized settings
   - Single source of truth
   - Easy parameter tuning

4. Observer/Update Pattern
   - Ecosystem updates animals
   - Simulation orchestrates all systems
   - Clean call hierarchy

5. Type Hints with TYPE_CHECKING
   - Prevents circular imports
   - Enables IDE autocomplete
   - Forward declarations for type hints

6. Entity Component System (implicit)
   - Animals have position, energy, type
   - Behaviors applied independently
   - Composition over inheritance
"""
