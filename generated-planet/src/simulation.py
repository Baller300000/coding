"""Main simulation - orchestrates all modules"""

import pygame
from .rendering.camera import Camera
from .rendering.renderer import Renderer
from .rendering.effects import ParticleEffects
from .ui.hud import HUD, Minimap, Stats
from .engine.input_handler import InputHandler
from .core.ecosystem import Ecosystem
from .engine.behaviors import BehaviorEngine, ReproductionEngine
from .utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS

class PlanetSimulation:
    """Main simulation class - orchestrates all systems"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("3D Planet Simulation - Animals & Terrain (v2.0: Enhanced Ecology)")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 18)
        
        # Initialize systems
        self.camera = Camera()
        self.renderer = Renderer(self.screen, self.camera)
        self.effects = ParticleEffects()
        self.hud = HUD(self.font)
        self.minimap = Minimap()
        self.stats = Stats(self.font)
        self.input_handler = InputHandler()
        self.ecosystem = Ecosystem()
        self.behavior_engine = BehaviorEngine()
        self.camera_mode = "normal"  # normal, follow, top-down
        self.reproduction_engine = ReproductionEngine()
        
        # State
        self.paused = False
        self.show_debug = True
    
    def handle_input(self) -> bool:
        """Handle all input"""
        if not self.input_handler.handle_events():
            return False
        
        # Continuous camera movement
        self.input_handler.update_camera(self.camera)
        
        # Key presses for discrete actions
        keys = self.input_handler.get_key_presses()
        
        for key in keys:
            if key == pygame.K_ESCAPE:
                return False
            elif key == pygame.K_p:
                self.paused = not self.paused
            elif key == pygame.K_UP:
                self.camera.zoom_in()
            elif key == pygame.K_DOWN:
                self.camera.zoom_out()
            elif key == pygame.K_LEFT:
                self.camera.rotate_yaw(-0.1)
            elif key == pygame.K_RIGHT:
                self.camera.rotate_yaw(0.1)
            elif key == pygame.K_r:
                self.camera.rotate_pitch(-0.1)
            elif key == pygame.K_f:
                self.camera.rotate_pitch(0.1)
            elif key == pygame.K_h:
                self.show_debug = not self.show_debug
            elif key == pygame.K_c:  # Switch camera mode
                modes = ["normal", "follow", "top-down"]
                current_idx = modes.index(self.camera_mode)
                self.camera_mode = modes[(current_idx + 1) % len(modes)]
            elif key == pygame.K_d:  # Create disease outbreak
                if self.ecosystem.animals:
                    from .core.health import HealthSystem
                    import random
                    patient = random.choice(self.ecosystem.animals)
                    self.ecosystem.health_system.create_outbreak(self.ecosystem.animals, patient)
            elif key == pygame.K_e:  # Trigger particle effects demo
                for _ in range(10):
                    self.effects.blood_splash(600 + 200 * self.clock.get_fps() % 200, 400)
        
        return True
    
    def update(self):
        """Update simulation"""
        if not self.paused:
            self.ecosystem.update(self.behavior_engine, self.reproduction_engine)
            self.stats.update(self.ecosystem.get_animal_counts())
    
    def draw(self):
        """Draw everything"""
        # Get weather effects
        brightness = self.ecosystem.weather.get_brightness()
        weather_type = self.ecosystem.weather.current_weather
        
        # Render scene
        self.renderer.render_scene(self.ecosystem.planet, self.ecosystem.animals)
        
        # Draw weather effects
        if weather_type == "rain":
            self.effects.rain_particles(1200, 800, brightness)
        elif weather_type == "snow":
            self.effects.snow_particles(1200, 800, 1 - brightness)
        
        # Draw particles
        self.effects.update()
        self.effects.draw(self.screen)
        
        # Draw UI
        if self.show_debug:
            animal_counts = self.ecosystem.get_animal_counts()
            breeding_count = self.ecosystem.get_breeding_count()
            season = self.ecosystem.weather.get_season()
            weather = self.ecosystem.weather.current_weather
            temp = int(self.ecosystem.weather.temperature)
            
            self.hud.draw_info(
                self.screen,
                int(self.clock.get_fps()),
                self.ecosystem.get_time_seconds(),
                self.ecosystem.get_total_animals(),
                animal_counts,
                self.paused,
                breeding_count
            )
            
            species_end_y = self.hud.draw_species_list(self.screen, animal_counts)
            self.hud.draw_controls(self.screen, species_end_y + 20)
            
            # Draw minimap
            self.minimap.draw(self.screen, self.camera.position, self.ecosystem.animals, self.ecosystem.planet)
        
        self.renderer.update_display()
    
    def run(self):
        """Main simulation loop"""
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
