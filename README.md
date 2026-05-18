<div align="center">

<img src="assets/banner.png" alt="Inteligência Ambiental Brasileira" width="100%"/>

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
> do CSV bruto do IBAMA ao shapefile com Índice Composto de Risco georreferenciado, pronto para QGIS e Power BI.

</div>

---

## Sobre o Projeto

Os autos de infração ambiental emitidos pelo IBAMA são documentos públicos que registram crimes contra Flora, Fauna, Qualidade Ambiental, Licenciamento e Controle Ambiental em todo o território brasileiro. Individualmente, cada registro é um dado. Agregados e georreferenciados, revelam **onde a pressão humana sobre o território é mais intensa, recorrente e economicamente significativa**.

Este projeto transforma os CSVs brutos disponíveis em [dadosabertos.ibama.gov.br](https://dadosabertos.ibama.gov.br) em seis camadas geoespaciais temáticas — com destaque para o `heat_indice_composto.shp`, que aplica um **Índice Composto de Risco (0–100)** ponderando tipo de infração, gravidade e valor de multa sobre cada um dos 2.710 registros georreferenciados.

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
| Período analisado | **2016 – 2026** |
| Registros no shapefile final | **2.710 pontos** · EPSG:4326 |

---

## Principais Insights

**1 · Flora é a categoria com maior valor acumulado de multas**  
Entre todas as tipologias — Flora, Administração Ambiental, Licenciamento, Qualidade Ambiental e Controle Ambiental —, as infrações contra a Flora concentram o maior volume financeiro de penalidades. Cada autuação representa supressão ou degradação direta de vegetação nativa.

**2 · O Arco Norte concentra a pressão máxima**  
Pará (PA), Amazonas (AM), Mato Grosso (MT) e Rondônia (RO) lideram em volume acumulado de multas. Os quatro estados formam o epicentro da crise de desmatamento — e os maiores valores do Índice Composto de Risco do projeto.

**3 · 72% dos infratores são Pessoas Físicas**  
O crime ambiental brasileiro não é majoritariamente corporativo: é difuso, pulverizado e cotidiano. Pessoas Jurídicas, apesar de minoria em volume, concentram os maiores valores médios de multa individual — exigindo estratégias de fiscalização distintas para cada perfil.

**4 · Amazônia lidera o Índice Composto**  
Com Índice médio de 82/100 e classificação **Muito Alto Risco**, a Amazônia é o bioma com maior pressão combinada de volume, gravidade e valor de infrações. A Mata Atlântica (71) e o Cerrado (58) completam o topo da escala.

**5 · 10% das infrações, impacto desproporcional**  
Apenas 1 em cada 10 registros é classificado pelo IBAMA como de Alta Gravidade — mas esse subconjunto exerce impacto desproporcional no Índice Composto e define as zonas de Muito Alto Risco no mapa.

---

## Metodologia · Índice Composto de Risco

O Índice Composto de Risco vai além da contagem bruta de ocorrências. Ele sintetiza três dimensões independentes em uma única métrica espacial — permitindo comparar a intensidade real da pressão ambiental entre territórios.

```
ÍNDICE = (0.30 × norm_tipo + 0.30 × norm_gravidade + 0.40 × norm_valor) × 100
```

| Dimensão | Coluna de origem | Peso | Critério de normalização |
|----------|-----------------|------|--------------------------|
| Tipo de Infração | `TIPO_AUTO` | 30% | Frequência relativa por categoria |
| Gravidade oficial | `GRAVIDADE_` | 30% | Leve=1 · Médio=2 · Grave=3 · Gravíssimo=4 |
| Valor da multa | `VAL_AUTO_I` | 40% | Min-max normalização (0–1) |

O peso maior sobre o valor da multa (40%) reflete que a penalidade financeira é o indicador mais direto e padronizado da magnitude do dano reconhecido pelo IBAMA.

### Classes de Risco

| Faixa | Classe | `classe_ris` |
|-------|--------|-------------|
| 80 – 100 | 🔴 Muito Alto | `Muito Alto` |
| 60 – 80  | 🟠 Alto       | `Alto`       |
| 40 – 60  | 🟡 Médio      | `Médio`      |
| 20 – 40  | 🟢 Baixo      | `Baixo`      |
|  0 – 20  | ⚪ Muito Baixo | `Muito Baixo` |

---

## Estrutura do Repositório

```
Inteligencia-Ambiental-Brasileira/
│
├── README.md
├── requirements.txt
│
├── Downloads/
│   ├── auto_infracao_csv/              ← CSVs brutos do IBAMA (não versionados)
│   │   └── auto_infracao_ano_*.csv
│   │
│   └── github.arquivos/                ← Scripts do pipeline
│       ├── extract_auto_infracao_coords.py
│       ├── prepare_heat_map_layers.py
│       ├── validar_heat_map_layers.py
│       └── create_qgis_zip.py
│
├── output/
│   └── heat_map_layers/
│       ├── heat_indice_composto.shp    ← CAMADA PRINCIPAL · 2.710 registros
│       ├── heat_indice_composto.geojson
│       ├── heat_tipo_auto.shp
│       ├── heat_gravidade.shp
│       ├── heat_valor.shp
│       ├── heat_municipios_agregado.shp
│       ├── heat_municipios_agregado.geojson
│       ├── heat_grid_density.shp
│       └── heat_grid_density.geojson
│
├── powerbi/
│   └── Monitor_IBAMA_2025.pbix
│
└── assets/
    ├── banner.png
    ├── mapa_biomas_autos_infracao.png
    ├── mapa_biomas.png
    └── dashboard_powerbi.png
```

---

## Camadas Geoespaciais

O pipeline gera **6 camadas temáticas** em Shapefile e GeoJSON:

| Arquivo | Registros | Descrição |
|---------|-----------|-----------|
| `heat_indice_composto.shp` | **2.710** | Índice Composto 0–100 · **camada recomendada** |
| `heat_tipo_auto.shp` | variável | Peso por frequência de tipo de infração |
| `heat_gravidade.shp` | variável | Peso por nível de gravidade IBAMA |
| `heat_valor.shp` | variável | Impacto financeiro normalizado em quintis |
| `heat_municipios_agregado.shp` | variável | Agregação por município · centróide |
| `heat_grid_density.shp` | variável | Grid 0,5° × 0,5° de densidade de ocorrências |

### Dicionário — `heat_indice_composto.shp`

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `TIPO_AUTO` | string | Categoria da infração (Flora, Fauna, Pesca…) |
| `GRAVIDADE_` | string | Gravidade oficial IBAMA |
| `VAL_AUTO_NUM` | float | Valor da multa em R$ |
| `indice_ris` | float | **Índice Composto de Risco (0–100)** ← coluna principal |
| `classe_ris` | string | Classe textual (Muito Baixo → Muito Alto) |
| `DES_LOCAL_` | string | Descrição textual do local da infração |
| `MUNICIPIO` | string | Município da autuação |
| `UF` | string | Unidade Federativa |
| `geometry` | Point | EPSG:4326 · lon/lat decimal |

**Cobertura espacial:**

```
Longitude: -70.0000° a -1.5667°  (de AM/AC até costa nordestina)
Latitude:  -33.6797° a  59.9833° (de RS até norte amazônico)
Projeção:  EPSG:4326 · SIRGAS 2000 · Zona 23S · Escala 1:390.000
```

---

## Scripts do Pipeline

### `extract_auto_infracao_coords.py`

Lê os arquivos `auto_infracao_ano_*.csv` do IBAMA, resolve coordenadas com dupla estratégia e exporta o shapefile base.

**Colunas de origem utilizadas:**

| Coluna CSV | Uso |
|-----------|-----|
| `NUM_LATITUDE_AUTO` | Coordenada Y principal |
| `NUM_LONGITUDE_AUTO` | Coordenada X principal |
| `DS_WKT` | Geometria WKT · fallback quando lat/lon ausente |
| `WKT_GE_AREA_AUTUADA` | Polígono da área autuada · fallback secundário |
| `DT_FATO_INFRACIONAL` | Data do fato · filtro temporal (prioridade 1) |
| `DT_INICIO_ATO_INEQUIVOCO` | Data início · filtro temporal (prioridade 2) |
| `DT_LANCAMENTO` | Data de lançamento · filtro temporal (prioridade 3) |

**Execução:**

```bash
python extract_auto_infracao_coords.py \
  --data-dir ./Downloads/auto_infracao_csv \
  --output-dir ./output \
  --format shp \
  --years 15
```

| Argumento | Padrão | Descrição |
|-----------|--------|-----------|
| `--data-dir` | diretório do script | Pasta com os CSVs `auto_infracao_ano_*.csv` |
| `--output-dir` | `./output` | Pasta de saída |
| `--format` | `geojson` | Formato: `geojson` · `shp` · `csv` |
| `--years` | `15` | Janela temporal de anos a incluir |
| `--date-column` | automático | Forçar coluna de data específica |

**Lógica de resolução de geometria:**

```
1. Tenta NUM_LATITUDE_AUTO + NUM_LONGITUDE_AUTO  →  Point direto
2. Se ausente: tenta DS_WKT                      →  parse WKT
3. Se ausente: tenta WKT_GE_AREA_AUTUADA         →  centróide do polígono
4. Registros sem geometria → salvo em invalid_auto_infracao_rows.csv
```

---

### `prepare_heat_map_layers.py`

Recebe o shapefile base e gera as 6 camadas temáticas com normalização min-max e o Índice Composto.

**Transformações aplicadas:**

```python
# TIPO_AUTO — peso por frequência relativa
gdf['peso_tipo_norm'] = minmax(tipo_counts[TIPO_AUTO]) * 100

# GRAVIDADE_ — mapeamento ordinal
gravidade_map = {'Leve': 1, 'Médio': 2, 'Grave': 3, 'Gravíssimo': 4}
gdf['peso_grav_norm'] = minmax(gravidade_num) * 100

# VAL_AUTO_I — normalização direta do valor financeiro
gdf['norm_val'] = minmax(VAL_AUTO_NUM)

# ÍNDICE COMPOSTO
indice = (0.30 * norm_tipo + 0.30 * norm_grav + 0.40 * norm_val) * 100
classe = pd.cut(indice, bins=[0,20,40,60,80,100],
                labels=['Muito Baixo','Baixo','Médio','Alto','Muito Alto'])
```

**Grid de densidade:**  
Células de 0,5° × 0,5° sobre o território nacional. Apenas células com ao menos 1 ocorrência são exportadas. Intensidade normalizada de 0 a 100 na coluna `intensity`.

---

### `validar_heat_map_layers.py`

QA automatizado dos outputs. Verifica para cada camada: existência do arquivo, integridade das geometrias, completude de colunas e estatísticas do `indice_ris`.

**O que é validado:**

- `heat_tipo_auto.shp` — Densidade por Tipo de Auto  
- `heat_gravidade.shp` — Densidade por Gravidade  
- `heat_valor.shp` — Densidade por Valor  
- `heat_indice_composto.shp` — Índice Composto (Principal)  
- `heat_municipios_agregado.shp` — Agregação por Município  
- `heat_grid_density.shp` — Grid de Densidade  

---

### `create_qgis_zip.py`

Empacota todo o conteúdo de `output/` em `output_qgis_files.zip` para distribuição.

```bash
python create_qgis_zip.py
# → Gera: output_qgis_files.zip
```

---

## Como Usar

### 1. Clonar e instalar

```bash
git clone https://github.com/marcosengdados/Inteligencia-Ambiental-Brasileira.git
cd Inteligencia-Ambiental-Brasileira
pip install -r requirements.txt
```

### 2. Baixar os dados brutos

Acesse [dadosabertos.ibama.gov.br](https://dadosabertos.ibama.gov.br) e baixe os arquivos `auto_infracao_ano_*.csv`. Coloque-os em `Downloads/auto_infracao_csv/`.

### 3. Executar o pipeline

```bash
# Passo 1 — extrair coordenadas e gerar shapefile base
python Downloads/github.arquivos/extract_auto_infracao_coords.py \
  --data-dir Downloads/auto_infracao_csv \
  --output-dir output \
  --format shp \
  --years 15

# Passo 2 — gerar as 6 camadas temáticas
python Downloads/github.arquivos/prepare_heat_map_layers.py

# Passo 3 — validar os outputs
python Downloads/github.arquivos/validar_heat_map_layers.py

# Passo 4 — empacotar para distribuição (opcional)
python Downloads/github.arquivos/create_qgis_zip.py
```

### 4. Abrir no QGIS

```
Layer → Add Layer → Add Vector Layer
Selecione: output/heat_map_layers/heat_indice_composto.shp

Properties → Symbology:
  Tipo:       Graduated
  Column:     indice_ris
  Color ramp: RdYlGn_r
  Mode:       Quantiles (Equal Count)
  Classes:    5
  → Classify → Apply
```

### 5. Abrir o Dashboard

Abra `powerbi/Monitor_IBAMA_2025.pbix` no Power BI Desktop.

---

## Dependências

```
pandas
geopandas
shapely
numpy
```

```bash
pip install -r requirements.txt
```

---

## Visualizações

<div align="center">

### Mapa de Autos de Infração · Biomas × Índice Composto de Risco
![Mapa QGIS](assets/mapa_biomas_autos_infracao.png)
*2.710 pontos · 6 biomas · Classes de risco Muito Baixo → Muito Alto · SIRGAS 2000 · Elaboração: Marcos Vinicius Lima*

### Monitor Power BI · Visão Integrada 2025
![Dashboard](assets/dashboard_powerbi.png)
*16,3 Mil autuações · R$ 4,31 Bi · 27 UFs · PA · AM · MT · RO · PR*

</div>

---

## Fontes

| Fonte | Uso no projeto |
|-------|---------------|
| [IBAMA · Dados Abertos](https://dadosabertos.ibama.gov.br) | Dataset `auto_infracao_ano_*.csv` — origem de todos os registros |
| [INPE](https://www.inpe.br) | Referência de biomas e dados territoriais |
| [Google Maps 2026](https://maps.google.com) | Basemap para composição cartográfica no QGIS |

---

## Autor

**Marcos Vinicius Lima**  
Análise de Dados Ambientais · Geoprocessamento · Power BI

[![LinkedIn](https://img.shields.io/badge/LinkedIn-marcosengdados-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/marcosengdados)
[![GitHub](https://img.shields.io/badge/GitHub-marcosengdados-181717?style=flat-square&logo=github)](https://github.com/marcosengdados)

---

## Licença

Os dados são provenientes de fontes públicas do IBAMA, disponibilizados sob a Lei de Acesso à Informação (Lei nº 12.527/2011).  
Os scripts e análises deste repositório estão licenciados sob [MIT License](LICENSE).
