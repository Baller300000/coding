"""Input handler module - manages user input"""

import pygame
from ..utils.constants import CAMERA_SPEED

class InputHandler:
    """Handles all user input"""
    
    def __init__(self):
        self.keys_pressed = {}
    
    def handle_events(self) -> bool:
        """Process all events. Returns False if quit requested"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                self.keys_pressed[event.key] = True
            elif event.type == pygame.KEYUP:
                self.keys_pressed[event.key] = False
        
        return True
    
    def is_key_pressed(self, key: int) -> bool:
        """Check if key is pressed"""
        return self.keys_pressed.get(key, False)
    
    def update_camera(self, camera):
        """Update camera based on input"""
        if self.is_key_pressed(pygame.K_w):
            camera.move_forward(CAMERA_SPEED)
        if self.is_key_pressed(pygame.K_s):
            camera.move_backward(CAMERA_SPEED)
        if self.is_key_pressed(pygame.K_a):
            camera.move_left(CAMERA_SPEED)
        if self.is_key_pressed(pygame.K_d):
            camera.move_right(CAMERA_SPEED)
        if self.is_key_pressed(pygame.K_SPACE):
            camera.move_up(CAMERA_SPEED * 0.5)
        if self.is_key_pressed(pygame.K_LSHIFT):
            camera.move_down(CAMERA_SPEED * 0.5)
    
    def get_key_presses(self) -> dict:
        """Get all currently pressed keys"""
        return {k: v for k, v in self.keys_pressed.items() if v}
