from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
from enum import Enum


class NodeType(Enum):
    JUNCTION = "JUNCTION"
    RESERVOIR = "RESERVOIR"
    TANK = "TANK"


class LinkType(Enum):
    PIPE = "PIPE"
    PUMP = "PUMP"
    VALVE = "VALVE"


@dataclass
class Coordinate:
    """Representa coordenadas X, Y de um elemento"""
    x: float
    y: float
    
    def to_dict(self) -> Dict[str, float]:
        return {"x": self.x, "y": self.y}


@dataclass
class Junction:
    """Representa um nó de junção"""
    id: str
    elevation: float
    demand: float
    demand_pattern: Optional[str] = None
    coordinates: Optional[Coordinate] = None
    
    def to_dict(self) -> Dict[str, Any]:
        data = {
            "id": self.id,
            "type": NodeType.JUNCTION.value,
            "elevation": self.elevation,
            "demand": self.demand,
            "demand_pattern": self.demand_pattern
        }
        if self.coordinates:
            data["coordinates"] = self.coordinates.to_dict()
        return data


@dataclass
class Reservoir:
    """Representa um reservatório"""
    id: str
    head: float
    head_pattern: Optional[str] = None
    coordinates: Optional[Coordinate] = None
    
    def to_dict(self) -> Dict[str, Any]:
        data = {
            "id": self.id,
            "type": NodeType.RESERVOIR.value,
            "head": self.head,
            "head_pattern": self.head_pattern
        }
        if self.coordinates:
            data["coordinates"] = self.coordinates.to_dict()
        return data


@dataclass
class Tank:
    """Representa um tanque"""
    id: str
    elevation: float
    init_level: float
    min_level: float
    max_level: float
    diameter: float
    min_volume: float
    volume_curve: Optional[str] = None
    coordinates: Optional[Coordinate] = None
    
    def to_dict(self) -> Dict[str, Any]:
        data = {
            "id": self.id,
            "type": NodeType.TANK.value,
            "elevation": self.elevation,
            "init_level": self.init_level,
            "min_level": self.min_level,
            "max_level": self.max_level,
            "diameter": self.diameter,
            "min_volume": self.min_volume,
            "volume_curve": self.volume_curve
        }
        if self.coordinates:
            data["coordinates"] = self.coordinates.to_dict()
        return data


@dataclass
class Pipe:
    """Representa um tubo"""
    id: str
    from_node: str
    to_node: str
    length: float
    diameter: float
    roughness: float
    minor_loss: float = 0.0
    status: str = "OPEN"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": LinkType.PIPE.value,
            "from_node": self.from_node,
            "to_node": self.to_node,
            "length": self.length,
            "diameter": self.diameter,
            "roughness": self.roughness,
            "minor_loss": self.minor_loss,
            "status": self.status
        }


@dataclass
class Pump:
    """Representa uma bomba"""
    id: str
    from_node: str
    to_node: str
    pump_curve: Optional[str] = None
    power: Optional[float] = None
    speed: float = 1.0
    pattern: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": LinkType.PUMP.value,
            "from_node": self.from_node,
            "to_node": self.to_node,
            "pump_curve": self.pump_curve,
            "power": self.power,
            "speed": self.speed,
            "pattern": self.pattern
        }


@dataclass
class Valve:
    """Representa uma válvula"""
    id: str
    from_node: str
    to_node: str
    diameter: float
    valve_type: str
    setting: float
    minor_loss: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": LinkType.VALVE.value,
            "from_node": self.from_node,
            "to_node": self.to_node,
            "diameter": self.diameter,
            "valve_type": self.valve_type,
            "setting": self.setting,
            "minor_loss": self.minor_loss
        }
