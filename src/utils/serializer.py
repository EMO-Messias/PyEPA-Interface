from typing import Any, Dict
import json


class NetworkSerializer:
    """Utilitários para serialização e desserialização de dados de rede"""
    
    @staticmethod
    def serialize(obj: Any) -> str:
        """
        Serializa um objeto para JSON
        
        Args:
            obj: Objeto com método to_dict()
            
        Returns:
            str: String JSON
        """
        if hasattr(obj, 'to_dict'):
            return json.dumps(obj.to_dict(), indent=2, ensure_ascii=False)
        return json.dumps(obj, indent=2, ensure_ascii=False)
    
    @staticmethod
    def deserialize(json_str: str) -> Dict[str, Any]:
        """
        Desserializa uma string JSON
        
        Args:
            json_str: String JSON
            
        Returns:
            Dict: Dicionário Python
        """
        return json.loads(json_str)
    
    @staticmethod
    def save_to_file(obj: Any, file_path: str) -> None:
        """
        Salva um objeto em arquivo JSON
        
        Args:
            obj: Objeto a ser salvo
            file_path: Caminho do arquivo
        """
        json_str = NetworkSerializer.serialize(obj)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(json_str)
    
    @staticmethod
    def load_from_file(file_path: str) -> Dict[str, Any]:
        """
        Carrega um objeto de arquivo JSON
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            Dict: Dicionário com os dados
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
