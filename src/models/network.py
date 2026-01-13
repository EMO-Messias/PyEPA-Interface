from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from .elements import Junction, Reservoir, Tank, Pipe, Pump, Valve


@dataclass
class Pattern:
    """Representa um padrão de demanda/operação"""
    id: str
    multipliers: List[float]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "multipliers": self.multipliers
        }


@dataclass
class Curve:
    """Representa uma curva (bomba, eficiência, volume, etc)"""
    id: str
    curve_type: str
    x_values: List[float]
    y_values: List[float]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.curve_type,
            "points": [{"x": x, "y": y} for x, y in zip(self.x_values, self.y_values)]
        }


@dataclass
class NetworkOptions:
    """Opções e configurações da rede"""
    headloss: str = "H-W"
    units: str = "GPM"
    pressure: str = "PSI"
    pattern: Optional[str] = None
    hydraulic_timestep: float = 1.0
    quality_timestep: float = 0.1
    duration: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "headloss": self.headloss,
            "units": self.units,
            "pressure": self.pressure,
            "pattern": self.pattern,
            "hydraulic_timestep": self.hydraulic_timestep,
            "quality_timestep": self.quality_timestep,
            "duration": self.duration
        }


@dataclass
class WaterNetwork:
    """Representa uma rede de água completa"""
    title: str = ""
    junctions: List[Junction] = field(default_factory=list)
    reservoirs: List[Reservoir] = field(default_factory=list)
    tanks: List[Tank] = field(default_factory=list)
    pipes: List[Pipe] = field(default_factory=list)
    pumps: List[Pump] = field(default_factory=list)
    valves: List[Valve] = field(default_factory=list)
    patterns: List[Pattern] = field(default_factory=list)
    curves: List[Curve] = field(default_factory=list)
    options: NetworkOptions = field(default_factory=NetworkOptions)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte toda a rede para um dicionário serializável"""
        return {
            "title": self.title,
            "nodes": {
                "junctions": [j.to_dict() for j in self.junctions],
                "reservoirs": [r.to_dict() for r in self.reservoirs],
                "tanks": [t.to_dict() for t in self.tanks]
            },
            "links": {
                "pipes": [p.to_dict() for p in self.pipes],
                "pumps": [p.to_dict() for p in self.pumps],
                "valves": [v.to_dict() for v in self.valves]
            },
            "patterns": [p.to_dict() for p in self.patterns],
            "curves": [c.to_dict() for c in self.curves],
            "options": self.options.to_dict(),
            "statistics": {
                "total_junctions": len(self.junctions),
                "total_reservoirs": len(self.reservoirs),
                "total_tanks": len(self.tanks),
                "total_pipes": len(self.pipes),
                "total_pumps": len(self.pumps),
                "total_valves": len(self.valves),
                "total_nodes": len(self.junctions) + len(self.reservoirs) + len(self.tanks),
                "total_links": len(self.pipes) + len(self.pumps) + len(self.valves)
            }
        }
