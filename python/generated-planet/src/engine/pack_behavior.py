"""Pack behavior and advanced AI"""

from typing import List, Optional, TYPE_CHECKING
from ..utils.vectors import Vector3
from ..utils.constants import PACK_FORMATION_DISTANCE, PACK_HUNT_BONUS

if TYPE_CHECKING:
    from ..core.animal import Animal

class Pack:
    """Represents a group of predators hunting together"""
    
    def __init__(self, leader: 'Animal'):
        self.members: List['Animal'] = [leader]
        self.leader = leader
        self.hunt_target: Optional[Vector3] = None
        self.formation_type = "line"  # line, circle, wedge
    
    def add_member(self, animal: 'Animal'):
        """Add member to pack"""
        if len(self.members) < 5:
            self.members.append(animal)
            animal.pack = self
    
    def remove_member(self, animal: 'Animal'):
        """Remove member from pack"""
        if animal in self.members:
            self.members.remove(animal)
            if animal == self.leader and self.members:
                self.leader = self.members[0]
    
    def get_formation_positions(self) -> dict:
        """Get target positions for each pack member"""
        positions = {}
        if self.formation_type == "line":
            for i, member in enumerate(self.members):
                offset = Vector3(i * 3 - 6, 0, i * 2)
                positions[member] = self.leader.position + offset
        elif self.formation_type == "circle":
            import math
            for i, member in enumerate(self.members):
                angle = (i / len(self.members)) * 2 * math.pi
                offset = Vector3(
                    math.cos(angle) * PACK_FORMATION_DISTANCE,
                    0,
                    math.sin(angle) * PACK_FORMATION_DISTANCE
                )
                positions[member] = self.leader.position + offset
        return positions
    
    def is_active(self) -> bool:
        """Check if pack is still viable"""
        return len(self.members) > 1

class PackBehavior:
    """Manages pack hunting and coordination"""
    
    @staticmethod
    def find_pack_nearby(animal: 'Animal', animals: List['Animal'], radius: float = 30) -> Optional[Pack]:
        """Find nearby pack of same predator type"""
        for other in animals:
            if (other.animal_type == animal.animal_type and 
                other.is_carnivore and 
                animal.position.distance_to(other.position) < radius):
                if hasattr(other, 'pack') and other.pack:
                    return other.pack
        return None
    
    @staticmethod
    def coordinate_pack_hunt(pack: Pack, target: Vector3, animals: List['Animal']) -> float:
        """Coordinate pack to hunt target, return damage bonus"""
        if not pack.is_active():
            return 1.0
        
        # Pack members close to target get bonus damage
        members_in_range = 0
        for member in pack.members:
            if member.position.distance_to(target) < 10:
                members_in_range += 1
        
        # More members = higher bonus
        return 1.0 + (members_in_range - 1) * PACK_HUNT_BONUS / len(pack.members)
    
    @staticmethod
    def defend_territory(animal: 'Animal', territory_center: Vector3, animals: List['Animal']):
        """Make animal defend territory from intruders"""
        for other in animals:
            if (other.animal_type == animal.animal_type and 
                other != animal and
                territory_center.distance_to(other.position) < 30):
                animal.aggression = 0.8
                return territory_center
        animal.aggression = 0.2
        return None
