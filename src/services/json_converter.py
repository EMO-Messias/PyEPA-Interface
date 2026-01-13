import json
from typing import Dict, Any
from ..models.network import WaterNetwork


class JsonConverter:
    """Classe para converter objetos de rede para JSON"""
    
    @staticmethod
    def network_to_json(network: WaterNetwork, indent: int = 2) -> str:
        """
        Converte um objeto WaterNetwork para JSON
        
        Args:
            network: Objeto WaterNetwork
            indent: Indentação do JSON
            
        Returns:
            str: String JSON formatada
        """
        network_dict = network.to_dict()
        return json.dumps(network_dict, indent=indent, ensure_ascii=False)
    
    @staticmethod
    def network_to_file(network: WaterNetwork, output_path: str, indent: int = 2) -> None:
        """
        Salva a rede em um arquivo JSON
        
        Args:
            network: Objeto WaterNetwork
            output_path: Caminho do arquivo de saída
            indent: Indentação do JSON
        """
        json_str = JsonConverter.network_to_json(network, indent)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(json_str)
    
    @staticmethod
    def json_to_dict(json_str: str) -> Dict[str, Any]:
        """
        Converte uma string JSON para dicionário
        
        Args:
            json_str: String JSON
            
        Returns:
            Dict: Dicionário Python
        """
        return json.loads(json_str)
    
    @staticmethod
    def file_to_dict(json_path: str) -> Dict[str, Any]:
        """
        Lê um arquivo JSON e retorna um dicionário
        
        Args:
            json_path: Caminho do arquivo JSON
            
        Returns:
            Dict: Dicionário Python
        """
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
