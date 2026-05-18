# Inteligência Ambiental Brasileira

Este projeto tem como objetivo analisar dados de **autos de infração ambiental** no Brasil, utilizando ferramentas como **Python, QGIS e Power BI** para gerar insights, mapas de calor e relatórios executivos.

## 🚀 Funcionalidades
- Processamento de arquivos CSV com dados históricos de autos de infração.
- Scripts em Python para limpeza, validação e análise dos dados.
- Geração de camadas geoespaciais (GeoJSON, SHP) para uso em QGIS.
- Criação de mapas de calor para identificar padrões de infrações ambientais.
- Relatórios executivos e recomendações para políticas públicas.

## 📂 Estrutura do Projeto
- `analises_seguras.py` → script de análise de dados.
- `prepare_heat_map_layers.py` → preparação das camadas de mapas de calor.
- `output/` → resultados gerados (GeoJSON, SHP, CSV).
- `docs/` → documentação e guias de uso.

## 🛠️ Tecnologias Utilizadas
- **Python 3.11+**
- **QGIS**
- **Power BI**
- **Git/GitHub**

## 📊 Exemplos de Uso
1. Executar análise de qualidade dos dados:
   ```bash
   python analyze_data_quality.py
