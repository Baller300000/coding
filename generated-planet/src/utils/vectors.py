import math
from dataclasses import dataclass

@dataclass
class Vector3:
    """3D vector class"""
    x: float
    y: float
    z: float
    
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __truediv__(self, scalar):
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)
    
    def normalize(self):
        length = self.length()
        if length == 0:
            return Vector3(0, 0, 0)
        return self / length
    
    def length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def distance_to(self, other):
        return (self - other).length()
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def to_tuple(self):
        return (self.x, self.y, self.z)

def rotate_x(point: Vector3, angle: float) -> Vector3:
    """Rotate point around X axis"""
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    y_rot = point.y * cos_a - point.z * sin_a
    z_rot = point.y * sin_a + point.z * cos_a
    return Vector3(point.x, y_rot, z_rot)

def rotate_y(point: Vector3, angle: float) -> Vector3:
    """Rotate point around Y axis"""
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    x_rot = point.x * cos_a + point.z * sin_a
    z_rot = -point.x * sin_a + point.z * cos_a
    return Vector3(x_rot, point.y, z_rot)

def rotate_z(point: Vector3, angle: float) -> Vector3:
    """Rotate point around Z axis"""
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    x_rot = point.x * cos_a - point.y * sin_a
    y_rot = point.x * sin_a + point.y * cos_a
    return Vector3(x_rot, y_rot, point.z)
