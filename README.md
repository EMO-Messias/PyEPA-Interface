# PyInterface - EPANET Network Reader

Projeto Python para leitura e conversão de arquivos INP (EPANET) para JSON estruturado.

## 📋 Características

- ✅ Leitura completa de arquivos INP do EPANET
- ✅ Extração de coordenadas dos elementos
- ✅ Estrutura orientada a objetos com classes bem definidas
- ✅ Conversão para JSON serializável
- ✅ Suporte a todos os elementos: junções, reservatórios, tanques, tubos, bombas e válvulas
- ✅ Extração de padrões, curvas e opções da rede
- ✅ Dados completamente serializáveis para uso em outros programas

## 🚀 Instalação

```bash
pip install -r requirements.txt
```

### Dependências

- `wntr` - Water Network Tool for Resilience (para leitura de arquivos INP)
- `epyt` - EPANET Python Toolkit
- `numpy` - Operações numéricas

## 💻 Uso Básico

```python
from src.services.inp_reader import InpReader
from src.services.json_converter import JsonConverter

# Lê o arquivo INP
reader = InpReader()
network = reader.read_inp_file("seu_arquivo.inp")

# Converte para JSON
json_output = JsonConverter.network_to_json(network)

# Salva em arquivo
JsonConverter.network_to_file(network, "output.json")
```

## 📁 Estrutura do Projeto

```
PyInterface/
├── src/
│   ├── __init__.py
│   ├── models/              # Modelos de dados
│   │   ├── __init__.py
│   │   ├── elements.py      # Classes dos elementos (nós e links)
│   │   └── network.py       # Classe da rede completa
│   ├── services/            # Serviços de leitura/conversão
│   │   ├── __init__.py
│   │   ├── inp_reader.py    # Leitor de arquivos INP
│   │   └── json_converter.py # Conversor para JSON
│   └── utils/               # Utilitários
│       ├── __init__.py
│       └── serializer.py    # Serialização/Desserialização
├── examples/
│   └── example_usage.py     # Exemplo de uso
├── tests/
│   └── __init__.py
├── requirements.txt
└── README.md
```

## 📊 Estrutura do JSON Gerado

```json
{
  "title": "Nome da Rede",
  "nodes": {
    "junctions": [
      {
        "id": "J1",
        "type": "JUNCTION",
        "elevation": 100.0,
        "demand": 50.0,
        "demand_pattern": "PAT1",
        "coordinates": {
          "x": 1000.0,
          "y": 2000.0
        }
      }
    ],
    "reservoirs": [...],
    "tanks": [...]
  },
  "links": {
    "pipes": [
      {
        "id": "P1",
        "type": "PIPE",
        "from_node": "J1",
        "to_node": "J2",
        "length": 1000.0,
        "diameter": 300.0,
        "roughness": 100.0,
        "minor_loss": 0.0,
        "status": "OPEN"
      }
    ],
    "pumps": [...],
    "valves": [...]
  },
  "patterns": [...],
  "curves": [...],
  "options": {...},
  "statistics": {
    "total_junctions": 10,
    "total_reservoirs": 1,
    "total_tanks": 2,
    "total_pipes": 15,
    "total_pumps": 1,
    "total_valves": 0,
    "total_nodes": 13,
    "total_links": 16
  }
}
```

## 🔍 Elementos Extraídos

### Nós (Nodes)

#### Junções (Junctions)
- ID do nó
- Elevação
- Demanda base
- Padrão de demanda
- **Coordenadas X, Y**

#### Reservatórios (Reservoirs)
- ID do nó
- Carga hidráulica (head)
- Padrão de variação de head
- **Coordenadas X, Y**

#### Tanques (Tanks)
- ID do nó
- Elevação
- Níveis (inicial, mínimo, máximo)
- Diâmetro
- Volume mínimo
- Curva de volume
- **Coordenadas X, Y**

### Links (Ligações)

#### Tubos (Pipes)
- ID do tubo
- Nó de origem
- Nó de destino
- Comprimento
- Diâmetro
- Rugosidade
- Perda de carga menor
- Status (OPEN/CLOSED)

#### Bombas (Pumps)
- ID da bomba
- Nó de origem
- Nó de destino
- Curva da bomba
- Potência
- Velocidade
- Padrão de operação

#### Válvulas (Valves)
- ID da válvula
- Nó de origem
- Nó de destino
- Diâmetro
- Tipo de válvula
- Configuração
- Perda de carga menor

### Outros Elementos

- **Padrões (Patterns)**: Multiplicadores ao longo do tempo
- **Curvas (Curves)**: Curvas de bomba, eficiência, volume
- **Opções (Options)**: Configurações da simulação

## 📝 Exemplo de Uso Completo

```python
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.inp_reader import InpReader
from src.services.json_converter import JsonConverter

# Lê o arquivo
reader = InpReader()
network = reader.read_inp_file("example.inp")

# Acessa dados específicos
for junction in network.junctions:
    print(f"Junção: {junction.id}")
    if junction.coordinates:
        print(f"  Coordenadas: ({junction.coordinates.x}, {junction.coordinates.y})")
    print(f"  Elevação: {junction.elevation}")
    print(f"  Demanda: {junction.demand}")

# Salva como JSON
JsonConverter.network_to_file(network, "network.json", indent=2)

# Carrega de volta
data = JsonConverter.file_to_dict("network.json")
print(f"Total de nós: {data['statistics']['total_nodes']}")
```

## 🔄 Serialização e Desserialização

Todos os objetos possuem métodos `to_dict()` que retornam dicionários Python padrão, facilmente serializáveis para JSON. Isso garante compatibilidade total para uso em outros programas.

```python
# Serialização
network_dict = network.to_dict()
json_string = JsonConverter.network_to_json(network)

# Desserialização
loaded_dict = JsonConverter.file_to_dict("network.json")
```

## 🎯 Coordenadas

Todas as coordenadas são extraídas automaticamente do arquivo INP e estruturadas no formato:

```python
{
  "x": 1000.0,
  "y": 2000.0
}
```

Essencial para visualização gráfica e análise espacial da rede.

## 📦 Próximos Passos

Para expandir o projeto, você pode adicionar:

- Simulação hidráulica com EPANET
- Análise de qualidade da água
- Visualização gráfica da rede
- Otimização de rede
- Exportação para outros formatos

## 📄 Licença

MIT License

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

---

**Desenvolvido para facilitar a integração entre EPANET e outras aplicações via JSON**
