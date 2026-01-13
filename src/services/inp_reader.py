import wntr
from typing import Optional
from ..models.network import WaterNetwork, Pattern, Curve, NetworkOptions
from ..models.elements import (
    Junction, Reservoir, Tank, Pipe, Pump, Valve, Coordinate
)


class InpReader:
    """Classe para ler arquivos INP e converter para objetos Python"""
    
    def __init__(self):
        self.wn: Optional[wntr.network.WaterNetworkModel] = None
    
    def read_inp_file(self, inp_file_path: str) -> WaterNetwork:
        """
        Lê um arquivo INP e retorna um objeto WaterNetwork
        
        Args:
            inp_file_path: Caminho para o arquivo .inp
            
        Returns:
            WaterNetwork: Objeto contendo toda a rede
        """
        # Carrega o arquivo INP usando WNTR
        self.wn = wntr.network.WaterNetworkModel(inp_file_path)
        
        # Cria o objeto de rede
        network = WaterNetwork()
        
        # Extrai informações básicas
        network.title = self._get_title()
        
        # Extrai nós
        network.junctions = self._extract_junctions()
        network.reservoirs = self._extract_reservoirs()
        network.tanks = self._extract_tanks()
        
        # Extrai links
        network.pipes = self._extract_pipes()
        network.pumps = self._extract_pumps()
        network.valves = self._extract_valves()
        
        # Extrai padrões e curvas
        network.patterns = self._extract_patterns()
        network.curves = self._extract_curves()
        
        # Extrai opções
        network.options = self._extract_options()
        
        return network
    
    def _get_title(self) -> str:
        """Extrai o título da rede"""
        return self.wn.name if hasattr(self.wn, 'name') else ""
    
    def _get_coordinates(self, node_name: str) -> Optional[Coordinate]:
        """Obtém as coordenadas de um nó"""
        try:
            node = self.wn.get_node(node_name)
            if hasattr(node, 'coordinates') and node.coordinates is not None:
                x, y = node.coordinates
                return Coordinate(x=float(x), y=float(y))
        except:
            pass
        return None
    
    def _extract_junctions(self) -> list[Junction]:
        """Extrai todas as junções da rede"""
        junctions = []
        for name, junction in self.wn.junctions():
            j = Junction(
                id=name,
                elevation=float(junction.elevation),
                demand=float(junction.base_demand),
                demand_pattern=junction.demand_timeseries_list[0].pattern_name 
                    if junction.demand_timeseries_list and 
                       junction.demand_timeseries_list[0].pattern_name else None,
                coordinates=self._get_coordinates(name)
            )
            junctions.append(j)
        return junctions
    
    def _extract_reservoirs(self) -> list[Reservoir]:
        """Extrai todos os reservatórios da rede"""
        reservoirs = []
        for name, reservoir in self.wn.reservoirs():
            r = Reservoir(
                id=name,
                head=float(reservoir.head_timeseries.base_value),
                head_pattern=reservoir.head_timeseries.pattern_name 
                    if hasattr(reservoir.head_timeseries, 'pattern_name') else None,
                coordinates=self._get_coordinates(name)
            )
            reservoirs.append(r)
        return reservoirs
    
    def _extract_tanks(self) -> list[Tank]:
        """Extrai todos os tanques da rede"""
        tanks = []
        for name, tank in self.wn.tanks():
            t = Tank(
                id=name,
                elevation=float(tank.elevation),
                init_level=float(tank.init_level),
                min_level=float(tank.min_level),
                max_level=float(tank.max_level),
                diameter=float(tank.diameter),
                min_volume=float(tank.min_vol),
                volume_curve=tank.vol_curve_name if hasattr(tank, 'vol_curve_name') else None,
                coordinates=self._get_coordinates(name)
            )
            tanks.append(t)
        return tanks
    
    def _extract_pipes(self) -> list[Pipe]:
        """Extrai todos os tubos da rede"""
        pipes = []
        for name, pipe in self.wn.pipes():
            p = Pipe(
                id=name,
                from_node=pipe.start_node_name,
                to_node=pipe.end_node_name,
                length=float(pipe.length),
                diameter=float(pipe.diameter),
                roughness=float(pipe.roughness),
                minor_loss=float(pipe.minor_loss),
                status=str(pipe.status.name)
            )
            pipes.append(p)
        return pipes
    
    def _extract_pumps(self) -> list[Pump]:
        """Extrai todas as bombas da rede"""
        pumps = []
        for name, pump in self.wn.pumps():
            pump_obj = Pump(
                id=name,
                from_node=pump.start_node_name,
                to_node=pump.end_node_name,
                pump_curve=pump.pump_curve_name if hasattr(pump, 'pump_curve_name') else None,
                power=float(pump.power) if hasattr(pump, 'power') and pump.power else None,
                speed=float(pump.speed_timeseries.base_value) if hasattr(pump, 'speed_timeseries') else 1.0,
                pattern=pump.speed_timeseries.pattern_name 
                    if hasattr(pump, 'speed_timeseries') and 
                       hasattr(pump.speed_timeseries, 'pattern_name') else None
            )
            pumps.append(pump_obj)
        return pumps
    
    def _extract_valves(self) -> list[Valve]:
        """Extrai todas as válvulas da rede"""
        valves = []
        for name, valve in self.wn.valves():
            v = Valve(
                id=name,
                from_node=valve.start_node_name,
                to_node=valve.end_node_name,
                diameter=float(valve.diameter),
                valve_type=str(valve.valve_type),
                setting=float(valve.setting),
                minor_loss=float(valve.minor_loss) if hasattr(valve, 'minor_loss') else 0.0
            )
            valves.append(v)
        return valves
    
    def _extract_patterns(self) -> list[Pattern]:
        """Extrai todos os padrões da rede"""
        patterns = []
        for name, pattern in self.wn.patterns():
            p = Pattern(
                id=name,
                multipliers=[float(m) for m in pattern.multipliers]
            )
            patterns.append(p)
        return patterns
    
    def _extract_curves(self) -> list[Curve]:
        """Extrai todas as curvas da rede"""
        curves = []
        for name, curve in self.wn.curves():
            c = Curve(
                id=name,
                curve_type=str(curve.curve_type) if hasattr(curve, 'curve_type') else "UNKNOWN",
                x_values=[float(point[0]) for point in curve.points],
                y_values=[float(point[1]) for point in curve.points]
            )
            curves.append(c)
        return curves
    
    def _extract_options(self) -> NetworkOptions:
        """Extrai as opções da rede"""
        options = NetworkOptions()
        
        if hasattr(self.wn.options, 'headloss'):
            options.headloss = str(self.wn.options.headloss)
        if hasattr(self.wn.options.hydraulic, 'demand_model'):
            options.units = str(self.wn.options.hydraulic.demand_model)
        if hasattr(self.wn.options.time, 'hydraulic_timestep'):
            options.hydraulic_timestep = float(self.wn.options.time.hydraulic_timestep)
        if hasattr(self.wn.options.time, 'quality_timestep'):
            options.quality_timestep = float(self.wn.options.time.quality_timestep)
        if hasattr(self.wn.options.time, 'duration'):
            options.duration = float(self.wn.options.time.duration)
        
        return options
