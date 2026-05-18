<div align="center">

# Inteligência Ambiental Brasileira

**Análise geoespacial de Autos de Infração do IBAMA · 2016–2026**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![GeoPandas](https://img.shields.io/badge/GeoPandas-Spatial-139C5A?style=flat-square)](https://geopandas.org)
[![QGIS](https://img.shields.io/badge/QGIS-3.x-589632?style=flat-square&logo=qgis&logoColor=white)](https://qgis.org)
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?style=flat-square&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com)
[![Dados Abertos](https://img.shields.io/badge/Fonte-IBAMA%20Dados%20Abertos-00A86B?style=flat-square)](https://dadosabertos.ibama.gov.br)
[![Licença](https://img.shields.io/badge/Licença-MIT-blue?style=flat-square)](LICENSE)

<br/>

> Pipeline completo de extração, georreferenciamento e visualização de autos de infração ambiental —
> do CSV bruto do IBAMA ao shapefile com Índice Composto de Risco georreferenciado,
> pronto para QGIS e Power BI.

</div>

---

## Sobre o Projeto

Os autos de infração ambiental emitidos pelo IBAMA registram crimes contra Flora, Fauna, Qualidade Ambiental, Licenciamento e Controle Ambiental em todo o território brasileiro. Individualmente, cada registro é um dado. Agregados e georreferenciados, revelam **onde a pressão humana sobre o território é mais intensa, recorrente e economicamente significativa**.

Este projeto transforma os CSVs brutos de [dadosabertos.ibama.gov.br](https://dadosabertos.ibama.gov.br) em seis camadas geoespaciais temáticas — com destaque para o `heat_indice_composto.shp`, que aplica um **Índice Composto de Risco (0–100)** ponderando tipo de infração, gravidade e valor de multa sobre 2.710 registros georreferenciados.

---

## Dashboard · Monitor de Autuações 2025

![Dashboard Power BI](https://raw.githubusercontent.com/marcosengdados/Inteligencia-Ambiental-Brasileira/main/Downloads/github.arquivos/Projeto-IBAMA-autos-2025.png)

*Monitor integrado · Power BI · 16,3 Mil autuações · R$ 4,31 Bi em multas · 27 UFs · 6 biomas*

---

## Números do Dataset

| Métrica | Valor |
|---------|-------|
| Autuações registradas | **16.300** |
| Total de multas aplicadas | **R$ 4,31 bilhões** |
| Valor mediano por autuação | **R$ 16.000** |
| Infrações de alta gravidade | **10%** do total |
| Autos cancelados | **4%** |
| Pessoas Físicas | **72,24%** dos infratores |
| Pessoas Jurídicas | **27,47%** dos infratores |
| Cobertura geográfica | **27 UFs** · cobertura nacional |
| Período analisado | **2016–2026** |
| Registros no shapefile | **2.710 pontos** · EPSG:4326 |

---

## Visualizações e Insights

### Mapa · Autos de Infração por Bioma e Gravidade

![Mapa Biomas - Autos de Infração](https://raw.githubusercontent.com/marcosengdados/Inteligencia-Ambiental-Brasileira/main/Downloads/github.arquivos/Mapa%20Biomas%20-%20Autos%20de%20Infra%C3%A7%C3%A3o.png)

*2.710 pontos georreferenciados · Classes de gravidade Muito Baixo → Muito Alto · SIRGAS 2000 · Zona 23S · 1:390.000*  
*Elaboração: Marcos Vinicius Lima · Fontes: IBAMA, INPE, Google Maps (2026)*

---

### Os Seis Biomas Brasileiros · Território de Análise

![Mapa Biomas](https://raw.githubusercontent.com/marcosengdados/Inteligencia-Ambiental-Brasileira/main/Downloads/github.arquivos/Mapa%20Biomas.png)

*Amazônia · Cerrado · Mata Atlântica · Caatinga · Pantanal · Pampa · QGIS · IBAMA · INPE*

---

### Volume de Multas · Top 5 Estados

![Roadmap top 5 multas por estados](https://raw.githubusercontent.com/marcosengdados/Inteligencia-Ambiental-Brasileira/main/Downloads/github.arquivos/Roadmap%20top%205%20multas%20por%20estados.png)

*Treemap Power BI · PA · AM · MT · RO · PR · Acúmulo anual por valor de multa aplicada*

**1 · Flora domina o volume de multas**  
Infrações contra a Flora concentram o maior valor acumulado de penalidades — reflexo direto da crise do desmatamento nos biomas Amazônia e Cerrado.

**2 · O Arco Norte é o epicentro**  
Pará, Amazonas, Mato Grosso e Rondônia lideram em volume financeiro acumulado, formando a fronteira de maior pressão sobre a Amazônia.

**3 · 72% dos infratores são Pessoas Físicas**  
O crime ambiental brasileiro é difuso, pulverizado e cotidiano — não majoritariamente corporativo.

**4 · 10% das infrações, impacto desproporcional**  
Apenas 1 em cada 10 registros é classificado como Alta Gravidade pelo IBAMA, mas esse subconjunto define as zonas de Muito Alto Risco no Índice Composto.

---

### Distribuição por Tipo de Infração · Volume de Multas

![Distribuição por tipo de Infração](https://raw.githubusercontent.com/marcosengdados/Inteligencia-Ambiental-Brasileira/main/Downloads/github.arquivos/Distribui%C3%A7%C3%A3o%20por%20tipo%20de%20Infra%C3%A7%C3%A3o.pdf.png)

*Valor acumulado por categoria · Power BI · Flora > Adm. Ambiental > Licenciamento > Qualidade Ambiental > Controle Ambiental*

---

### Perfil do Infrator · Pessoa Física vs Jurídica

![Mapa Pizza % PF-PJ](https://raw.githubusercontent.com/marcosengdados/Inteligencia-Ambiental-Brasileira/main/Downloads/github.arquivos/Mapa%20Pizza%20%25%20PF-PJ.png)

*Distribuição do valor total de multas por tipo de pessoa · Power BI · PF 72,24% · PJ 27,47% · N.I. 0,28%*

---

## Metodologia · Índice Composto de Risco

O índice sintetiza três dimensões independentes em uma única métrica espacial, permitindo comparar a intensidade real da pressão ambiental entre territórios — além da simples contagem de ocorrências.

```
ÍNDICE = (0.30 × norm_tipo + 0.30 × norm_gravidade + 0.40 × norm_valor) × 100
```

| Dimensão | Coluna CSV | Peso | Normalização |
|----------|-----------|------|-------------|
| Tipo de Infração | `TIPO_AUTO` | 30% | Frequência relativa por categoria |
| Gravidade oficial | `GRAVIDADE_` | 30% | Leve=1 · Médio=2 · Grave=3 · Gravíssimo=4 |
| Valor da multa | `VAL_AUTO_I` | 40% | Min-max (0–1) |

O peso de 40% sobre o valor da multa reflete que a penalidade financeira é o indicador mais direto e padronizado da magnitude do dano reconhecido pelo IBAMA.

### Classes de Risco

| Faixa | Classe | `classe_ris` |
|-------|--------|-------------|
| 80–100 | 🔴 Muito Alto | `Muito Alto` |
| 60–80  | 🟠 Alto       | `Alto`       |
| 40–60  | 🟡 Médio      | `Médio`      |
| 20–40  | 🟢 Baixo      | `Baixo`      |
|  0–20  | ⚪ Muito Baixo | `Muito Baixo` |

---

## Estrutura do Repositório

```
Inteligencia-Ambiental-Brasileira/
│
├── README.md
├── requirements.txt
│
├── Downloads/
│   ├── auto_infracao_csv/                                    ← CSVs brutos IBAMA (não versionados)
│   │   └── auto_infracao_ano_*.csv
│   │
│   └── github.arquivos/                                      ← Scripts + imagens do projeto
│       ├── extract_auto_infracao_coords.py
│       ├── prepare_heat_map_layers.py
│       ├── validar_heat_map_layers.py
│       ├── create_qgis_zip.py
│       ├── Projeto-IBAMA-autos-2025.png
│       ├── Mapa Biomas - Autos de Infração.png
│       ├── Mapa Biomas.png
│       ├── Roadmap top 5 multas por estados.png
│       ├── Distribuição por tipo de Infração.pdf.png
│       └── Mapa Pizza % PF-PJ.png
│
├── output/
│   └── heat_map_layers/
│       ├── heat_indice_composto.shp                          ← CAMADA PRINCIPAL · 2.710 registros
│       ├── heat_indice_composto.geojson
│       ├── heat_tipo_auto.shp
│       ├── heat_gravidade.shp
│       ├── heat_valor.shp
│       ├── heat_municipios_agregado.shp
│       ├── heat_municipios_agregado.geojson
│       ├── heat_grid_density.shp
│       └── heat_grid_density.geojson
│
└── powerbi/
    └── Monitor_IBAMA_2025.pbix
```

---

## Camadas Geoespaciais

| Arquivo | Registros | Descrição |
|---------|-----------|-----------|
| `heat_indice_composto.shp` | **2.710** | Índice Composto 0–100 · **recomendada** |
| `heat_tipo_auto.shp` | variável | Peso por frequência de tipo de infração |
| `heat_gravidade.shp` | variável | Peso por nível de gravidade IBAMA |
| `heat_valor.shp` | variável | Impacto financeiro normalizado em quintis |
| `heat_municipios_agregado.shp` | variável | Agregação por município · centróide |
| `heat_grid_density.shp` | variável | Grid 0,5° × 0,5° de densidade |

### Dicionário · `heat_indice_composto.shp`

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `TIPO_AUTO` | string | Categoria da infração |
| `GRAVIDADE_` | string | Gravidade oficial IBAMA |
| `VAL_AUTO_NUM` | float | Valor da multa em R$ |
| `indice_ris` | float | **Índice Composto de Risco (0–100)** |
| `classe_ris` | string | Muito Baixo → Muito Alto |
| `DES_LOCAL_` | string | Descrição do local |
| `MUNICIPIO` | string | Município da autuação |
| `UF` | string | Unidade Federativa |
| `geometry` | Point | EPSG:4326 |

```
Extensão espacial:
  Longitude:  -70.0000° W  a  -1.5667° E
  Latitude:   -33.6797° S  a  59.9833° N
  Projeção:   EPSG:4326 · SIRGAS 2000 · Zona 23S · 1:390.000
```

---

## Scripts do Pipeline

### `extract_auto_infracao_coords.py`

Lê os CSVs brutos, resolve coordenadas com tripla estratégia de fallback e exporta o shapefile base.

**Colunas de origem utilizadas:**

| Coluna CSV | Uso |
|-----------|-----|
| `NUM_LATITUDE_AUTO` | Coordenada Y principal |
| `NUM_LONGITUDE_AUTO` | Coordenada X principal |
| `DS_WKT` | Geometria WKT · fallback primário |
| `WKT_GE_AREA_AUTUADA` | Polígono da área · fallback secundário |
| `DT_FATO_INFRACIONAL` | Filtro temporal (prioridade 1) |
| `DT_INICIO_ATO_INEQUIVOCO` | Filtro temporal (prioridade 2) |
| `DT_LANCAMENTO` | Filtro temporal (prioridade 3) |

```
Resolução de geometria:
1. NUM_LATITUDE_AUTO + NUM_LONGITUDE_AUTO  →  Point direto
2. DS_WKT                                  →  parse WKT
3. WKT_GE_AREA_AUTUADA                     →  centróide do polígono
4. Sem geometria                           →  invalid_auto_infracao_rows.csv
```

```bash
python Downloads/github.arquivos/extract_auto_infracao_coords.py \
  --data-dir Downloads/auto_infracao_csv \
  --output-dir output \
  --format shp \
  --years 15
```

| Argumento | Padrão | Opções |
|-----------|--------|--------|
| `--format` | `geojson` | `geojson` · `shp` · `csv` |
| `--years` | `15` | Janela temporal em anos |
| `--date-column` | automático | Forçar coluna de data específica |

---

### `prepare_heat_map_layers.py`

Gera as 6 camadas temáticas com normalização min-max e calcula o Índice Composto.

```python
# Ponderação do Índice Composto
indice_risco = (0.30 * norm_tipo + 0.30 * norm_grav + 0.40 * norm_val) * 100

# Classificação em 5 classes
classe_risco = pd.cut(indice_risco,
    bins=[0, 20, 40, 60, 80, 100],
    labels=['Muito Baixo', 'Baixo', 'Médio', 'Alto', 'Muito Alto'])

# Grid de densidade: células 0,5° × 0,5°
grid_density = create_density_grid(gdf, grid_size=0.5)
```

---

### `validar_heat_map_layers.py`

QA automatizado: verifica existência, integridade de geometrias e estatísticas do `indice_ris` para todas as 6 camadas geradas.

---

### `create_qgis_zip.py`

Empacota todo o conteúdo de `output/` em `output_qgis_files.zip` para distribuição.

```bash
python Downloads/github.arquivos/create_qgis_zip.py
# → output_qgis_files.zip
```

---

## Como Usar

```bash
# 1. Clonar e instalar
git clone https://github.com/marcosengdados/Inteligencia-Ambiental-Brasileira.git
cd Inteligencia-Ambiental-Brasileira
pip install -r requirements.txt

# 2. Baixar CSVs em dadosabertos.ibama.gov.br
#    → salvar em Downloads/auto_infracao_csv/

# 3. Executar pipeline
python Downloads/github.arquivos/extract_auto_infracao_coords.py \
  --data-dir Downloads/auto_infracao_csv --output-dir output --format shp --years 15

python Downloads/github.arquivos/prepare_heat_map_layers.py
python Downloads/github.arquivos/validar_heat_map_layers.py

# 4. Abrir no QGIS
#    Layer → Add Vector Layer → output/heat_map_layers/heat_indice_composto.shp
#    Symbology → Graduated → Column: indice_ris → RdYlGn_r → 5 classes → Classify

# 5. Empacotar para distribuição (opcional)
python Downloads/github.arquivos/create_qgis_zip.py
```

---

## Dependências

```
pandas>=1.5.0
geopandas>=0.12.0
shapely>=2.0.0
numpy>=1.23.0
```

```bash
pip install -r requirements.txt
```

---

## Fontes

| Fonte | Uso |
|-------|-----|
| [IBAMA · Dados Abertos](https://dadosabertos.ibama.gov.br) | Dataset `auto_infracao_ano_*.csv` |
| [INPE](https://www.inpe.br) | Referência de biomas e dados territoriais |
| [Google Maps 2026](https://maps.google.com) | Basemap para composição cartográfica QGIS |

---

## Autor

**Marcos Vinicius Lima**  
Análise de Dados Ambientais · Geoprocessamento · Power BI

[![LinkedIn](https://img.shields.io/badge/LinkedIn-marcosengdados-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/marcosengdados)
[![GitHub](https://img.shields.io/badge/GitHub-marcosengdados-181717?style=flat-square&logo=github)](https://github.com/marcosengdados)

---

## Licença

Dados provenientes de fontes públicas do IBAMA — Lei de Acesso à Informação (Lei nº 12.527/2011).  
Scripts e análises licenciados sob [MIT License](LICENSE).
