# 3D Planet Simulation with Animals & Terrain

A Python-based 3D ecosystem simulator featuring procedurally generated Minecraft-style terrain, diverse animal species with realistic behaviors, and a breeding system.

## Quick Start

### Run the Simulation

```bash
python main.py
```

### Controls

- **WASD** - Move camera
- **Space/Shift** - Move up/down
- **Arrow Keys** - Rotate view
- **R/F** - Tilt camera
- **Up/Down Arrows** - Zoom in/out
- **P** - Pause/Resume
- **H** - Toggle HUD info
- **ESC** - Quit

## Project Structure

The codebase is organized into a professional Python package structure for maintainability and scalability:

a```
src/
├── utils/              # Shared utilities (vectors, constants)
├── core/               # Core simulation (planet, animals, ecosystem)
├── rendering/          # Graphics (camera, renderer, sprites)
├── engine/             # Game logic (behaviors, input)
└── ui/                 # User interface (HUD, minimap)
a```

See `PROJECT_STRUCTURE.md` for detailed documentation of the package layout.

## Features

### World

- **3D Minecraft-style terrain** with procedurally generated terrain
- **Voxel-based blocks** with grass, dirt, stone, sand, water, and trees
- **Dynamic water** systems with lakes
- **Surface-only rendering** for performance (large worlds)
- **Chunk-based generation** for seamless terrain

### Animals

**10+ species with unique behaviors:**

- Herbivores: Rabbit, Deer, Mouse, Duck, Turtle
- Carnivores: Wolf, Fox, Eagle
- Omnivores: Bird
- Aquatic: Fish

Each species has:

- Custom movement speed and vision range
- Realistic behavior patterns (hunting, grazing, breeding)
- Energy management system
- Visual differentiation with species-specific sprites

### Simulation

- **Breeding System** - Animals reproduce when well-fed (magenta indicator)
- **Energy Management** - Animals consume energy through movement, gain it by eating
- **Population Dynamics** - Births and deaths create evolving ecosystems
- **AI Pathfinding** - Animals seek food and prey intelligently
- **Terrain Interaction** - Herbivores eat grass, all animals walk/swim appropriately

### Graphics

- **3D Perspective Projection** - Dynamic camera with rotation and zoom
- **Detailed Sprites** - 3D-looking animals with eyes, limbs, and special features
- **Depth Rendering** - Proper layering of terrain and objects
- **HUD System** - Real-time statistics, species list, minimap
- **Visual Feedback** - Energy bars, breeding indicators

## Technologies

- **Python 3.7+**
- **Pygame** - Graphics and event handling
- **Vector Mathematics** - Custom Vector3 class for 3D operations
- **Procedural Generation** - Terrain using Perlin-like noise

## Performance

Optimized for smooth gameplay:

- Render distance culling (only visible blocks drawn)
- Surface-only rendering (interior blocks hidden)
- Reduced world size (64x64 units) for responsiveness
- Efficient chunk generation system
- 60 FPS target

## Package Architecture

### `/src/utils/`

- `constants.py` - Global configuration and animal definitions
- `vectors.py` - Vector3 math class and rotation functions

### `/src/core/`

- `planet.py` - Terrain generation and block management
- `animal.py` - Animal entity class with behaviors
- `ecosystem.py` - World state and animal management

### `/src/rendering/`

- `camera.py` - 3D camera with projection
- `renderer.py` - Main graphics renderer
- `sprites.py` - Sprite drawing functions

### `/src/engine/`

- `behaviors.py` - Animal AI and reproduction logic
- `input_handler.py` - Input management

### `/src/ui/`

- `hud.py` - HUD, minimap, statistics

### `/src/simulation.py`

- Main orchestrator class that ties all systems together

## Extending the Project

The modular structure makes it easy to add new features:

1. **New Animal Types** - Add to `src/utils/constants.py` and implement in `Animal` class
2. **New Terrain Features** - Extend `Planet` class in `src/core/planet.py`
3. **UI Enhancements** - Add to `src/ui/hud.py`
4. **Rendering Effects** - Modify `src/rendering/renderer.py` or `sprites.py`
5. **New Behaviors** - Add methods to `BehaviorEngine` in `src/engine/behaviors.py`

## Notes

- All modules use relative imports from the src package
- The project follows Python packaging best practices
- Type hints are used throughout for better IDE support
- Circular dependencies are handled with TYPE_CHECKING imports

## License

Open source - feel free to use and modify!
