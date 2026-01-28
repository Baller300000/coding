"""Camera module - handles 3D projection and camera movement"""

import math
from ..utils.vectors import Vector3, rotate_x, rotate_y
from ..utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT, DEFAULT_ZOOM

class Camera:
    """3D camera for viewing the world"""
    
    def __init__(self):
        self.position = Vector3(0, 25, -40)
        self.rotation_x = 0.6
        self.rotation_y = 0
        self.zoom = DEFAULT_ZOOM
    
    def project_3d_to_2d(self, point: Vector3) -> tuple:
        """Project 3D point to 2D screen with perspective"""
        # Translate to camera position
        p = point - self.position
        
        # Apply rotations
        p = rotate_x(p, self.rotation_x)
        p = rotate_y(p, self.rotation_y)
        
        # Perspective projection
        if p.z < 0.1:
            return None
        
        scale = 300 / (p.z * self.zoom)
        x_2d = WINDOW_WIDTH // 2 + p.x * scale
        y_2d = WINDOW_HEIGHT // 2 - p.y * scale
        
        return (int(x_2d), int(y_2d), scale)
    
    def move_forward(self, speed: float):
        """Move forward in view direction"""
        forward = Vector3(math.sin(self.rotation_y), 0, -math.cos(self.rotation_y)) * speed
        self.position = self.position + forward
    
    def move_backward(self, speed: float):
        """Move backward"""
        forward = Vector3(math.sin(self.rotation_y), 0, -math.cos(self.rotation_y)) * speed
        self.position = self.position - forward
    
    def move_left(self, speed: float):
        """Move left"""
        right = Vector3(math.cos(self.rotation_y), 0, math.sin(self.rotation_y)) * speed
        self.position = self.position - right
    
    def move_right(self, speed: float):
        """Move right"""
        right = Vector3(math.cos(self.rotation_y), 0, math.sin(self.rotation_y)) * speed
        self.position = self.position + right
    
    def move_up(self, speed: float):
        """Move up"""
        self.position.y += speed
    
    def move_down(self, speed: float):
        """Move down"""
        self.position.y -= speed
    
    def rotate_yaw(self, angle: float):
        """Rotate around Y axis (horizontal look)"""
        self.rotation_y += angle
    
    def rotate_pitch(self, angle: float):
        """Rotate around X axis (vertical look)"""
        self.rotation_x = max(0.1, min(1.5, self.rotation_x + angle))
    
    def zoom_in(self, factor: float = 0.95):
        """Zoom in"""
        self.zoom *= factor
    
    def zoom_out(self, factor: float = 0.95):
        """Zoom out"""
        self.zoom /= factor
