"""
Exemplo de uso do leitor de arquivos INP
"""
import sys
import os

# Adiciona o diretório pai ao path para importar o módulo src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.inp_reader import InpReader
from src.services.json_converter import JsonConverter


def main():
    # Caminho para o arquivo INP
    inp_file_path = "D:\\YOUTUBE\\01 - CANAIS\\01 - OPENEPA\\exemplo-3.inp"
    # Cria o leitor
    reader = InpReader()
    # Lê o arquivo INP
    print(f"Lendo arquivo INP: {inp_file_path}")
    network = reader.read_inp_file(inp_file_path)
    # Converte para JSON
    json_output = JsonConverter.network_to_json(network, indent=2)  
    # Exibe estatísticas
    stats = network.to_dict()['statistics']
    print(f"\n=== Estatísticas da Rede ===")
    print(f"Total de Junções: {stats['total_junctions']}")
    print(f"Total de Reservatórios: {stats['total_reservoirs']}")
    print(f"Total de Tanques: {stats['total_tanks']}")
    print(f"Total de Tubos: {stats['total_pipes']}")
    print(f"Total de Bombas: {stats['total_pumps']}")
    print(f"Total de Válvulas: {stats['total_valves']}")
    # Salva em arquivo
    output_file = "network_output.json"
    JsonConverter.network_to_file(network, output_file, indent=2)
    print(f"\nArquivo JSON salvo em: {output_file}") 
    # Exemplo de como acessar dados específicos
    print(f"\n=== Exemplo de Dados ===")
    if network.junctions:
        first_junction = network.junctions[0]
        print(f"Primeira Junção: {first_junction.id}")
        print(f"  Elevação: {first_junction.elevation}")
        print(f"  Demanda: {first_junction.demand}")
        if first_junction.coordinates:
            print(f"  Coordenadas: X={first_junction.coordinates.x}, Y={first_junction.coordinates.y}")
    
    if network.pipes:
        first_pipe = network.pipes[0]
        print(f"\nPrimeiro Tubo: {first_pipe.id}")
        print(f"  De: {first_pipe.from_node} -> Para: {first_pipe.to_node}")
        print(f"  Comprimento: {first_pipe.length}")
        print(f"  Diâmetro: {first_pipe.diameter}")
    
    # Desserialização (lendo de volta)
    print(f"\n=== Teste de Desserialização ===")
    loaded_data = JsonConverter.file_to_dict(output_file)
    print(f"Dados carregados com sucesso!")
    print(f"Título da rede: {loaded_data.get('title', 'N/A')}")
    print(f"Total de nós: {loaded_data['statistics']['total_nodes']}")


if __name__ == "__main__":
    main()
