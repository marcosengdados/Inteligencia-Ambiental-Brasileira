"""
PREPARAÇÃO DE DADOS PARA ANÁLISE DE MAPAS DE CALOR NO QGIS
Integração: Tipo de Auto + Gravidade + Valor
"""
import pandas as pd
import geopandas as gpd
from pathlib import Path
import json
import numpy as np
from shapely.geometry import Point, box

print("=" * 100)
print("PREPARAÇÃO DE DADOS PARA MAPAS DE CALOR - QGIS")
print("=" * 100)

# ============================================================================
# 1. CARREGAMENTO DE DADOS
# ============================================================================
output_dir = Path("output")
print("\n1. Carregando dados do shapefile...")

gdf = gpd.read_file(output_dir / "auto_infracao_coords_valid.shp")
print(f"   Carregado: {len(gdf)} registros")

# Filtrar apenas os últimos 15 anos pelo campo parsed_dat
print("\n   Filtrando registros por data (últimos 15 anos)...")
gdf['parsed_dat'] = pd.to_datetime(gdf['parsed_dat'], errors='coerce')
max_date = gdf['parsed_dat'].max()
cutoff_date = max_date - pd.DateOffset(years=15)
initial_len = len(gdf)
gdf = gdf[gdf['parsed_dat'] >= cutoff_date].copy()
print(f"   Período: {cutoff_date.date()} até {max_date.date()}")
print(f"   Registros antes do filtro: {initial_len}")
print(f"   Registros após o filtro: {len(gdf)}")
if gdf['parsed_dat'].isna().any():
    print(f"   AVISO: Registros sem data válida: {gdf['parsed_dat'].isna().sum()} (excluídos do filtro)")

# ============================================================================
# 2. ANÁLISE DAS COLUNAS RELEVANTES
# ============================================================================
print("\n2. Análise das colunas para mapa de calor:")
print("-" * 100)

# TIPO_AUTO
print(f"\n   A) TIPO_AUTO ({gdf['TIPO_AUTO'].notna().sum()}/{len(gdf)} = {(gdf['TIPO_AUTO'].notna().sum()/len(gdf))*100:.1f}%)")
tipo_auto_dist = gdf[gdf['TIPO_AUTO'].notna()]['TIPO_AUTO'].value_counts()
print("      Distribuição:")
for tipo, count in tipo_auto_dist.head(10).items():
    print(f"        - {tipo}: {count}")

# GRAVIDADE
print(f"\n   B) GRAVIDADE_ ({gdf['GRAVIDADE_'].notna().sum()}/{len(gdf)} = {(gdf['GRAVIDADE_'].notna().sum()/len(gdf))*100:.1f}%)")
gravidade_dist = gdf[gdf['GRAVIDADE_'].notna()]['GRAVIDADE_'].value_counts()
print("      Distribuição:")
for grav, count in gravidade_dist.head(10).items():
    print(f"        - {grav}: {count}")

# VALOR
print(f"\n   C) VAL_AUTO_I ({gdf['VAL_AUTO_I'].notna().sum()}/{len(gdf)} = {(gdf['VAL_AUTO_I'].notna().sum()/len(gdf))*100:.1f}%)")
gdf['VAL_AUTO_NUM'] = pd.to_numeric(gdf['VAL_AUTO_I'].str.replace(',', '.'), errors='coerce')
val_stats = gdf[gdf['VAL_AUTO_NUM'].notna()]['VAL_AUTO_NUM']
print(f"      Valor mínimo: R$ {val_stats.min():,.2f}")
print(f"      Valor máximo: R$ {val_stats.max():,.2f}")
print(f"      Valor médio: R$ {val_stats.mean():,.2f}")
print(f"      Valor total: R$ {val_stats.sum():,.2f}")

# ============================================================================
# 3. CRIAÇÃO DE CAMADAS TEMÁTICAS PARA CALOR
# ============================================================================
print("\n3. Criando camadas de análise para mapas de calor:")
print("-" * 100)

# Criar diretório para outputs
heat_dir = output_dir / "heat_map_layers"
heat_dir.mkdir(exist_ok=True)

# *** CAMADA 1: POR TIPO DE AUTO ***
print("\n   CAMADA 1: Densidade por TIPO_AUTO")
gdf_tipo = gdf[gdf['TIPO_AUTO'].notna()].copy()

# Adicionar peso por tipo (contagem)
tipo_counts = gdf_tipo['TIPO_AUTO'].value_counts()
gdf_tipo['peso_tipo'] = gdf_tipo['TIPO_AUTO'].map(tipo_counts)

# Normalizar para 0-100
gdf_tipo['peso_tipo_norm'] = (gdf_tipo['peso_tipo'] - gdf_tipo['peso_tipo'].min()) / (gdf_tipo['peso_tipo'].max() - gdf_tipo['peso_tipo'].min()) * 100

# Salvar
output_tipo = heat_dir / "heat_tipo_auto.shp"
gdf_tipo[['TIPO_AUTO', 'peso_tipo', 'peso_tipo_norm', 'DES_LOCAL_', 'MUNICIPIO', 'UF', 'geometry']].to_file(output_tipo)
print(f"      Salvo em: {output_tipo}")

# *** CAMADA 2: POR GRAVIDADE ***
print("\n   CAMADA 2: Densidade por GRAVIDADE")
gdf_grav = gdf[gdf['GRAVIDADE_'].notna()].copy()

# Criar mapeamento de gravidade para valor numérico
gravidade_map = {
    'Grave': 3,
    'Médio': 2,
    'Leve': 1,
    'Gravíssimo': 4,
}
gdf_grav['gravidade_num'] = gdf_grav['GRAVIDADE_'].map(gravidade_map)

# Contar ocorrências por gravidade
grav_counts = gdf_grav['GRAVIDADE_'].value_counts()
gdf_grav['peso_gravidade'] = gdf_grav['GRAVIDADE_'].map(grav_counts)
gdf_grav['peso_grav_norm'] = (gdf_grav['peso_gravidade'] - gdf_grav['peso_gravidade'].min()) / (gdf_grav['peso_gravidade'].max() - gdf_grav['peso_gravidade'].min()) * 100

# Salvar
output_grav = heat_dir / "heat_gravidade.shp"
gdf_grav[['GRAVIDADE_', 'gravidade_num', 'peso_gravidade', 'peso_grav_norm', 'DES_LOCAL_', 'MUNICIPIO', 'UF', 'geometry']].to_file(output_grav)
print(f"      Salvo em: {output_grav}")

# *** CAMADA 3: POR VALOR (IMPACTO FINANCEIRO) ***
print("\n   CAMADA 3: Densidade por VALOR")
gdf_val = gdf[gdf['VAL_AUTO_NUM'].notna()].copy()

# Normalizar valor para 0-100
gdf_val['peso_valor_norm'] = (gdf_val['VAL_AUTO_NUM'] - gdf_val['VAL_AUTO_NUM'].min()) / (gdf_val['VAL_AUTO_NUM'].max() - gdf_val['VAL_AUTO_NUM'].min()) * 100

# Categorizar em quintis
gdf_val['valor_quintil'] = pd.qcut(gdf_val['VAL_AUTO_NUM'], q=5, labels=['Muito Baixo', 'Baixo', 'Médio', 'Alto', 'Muito Alto'], duplicates='drop')

# Salvar
output_val = heat_dir / "heat_valor.shp"
gdf_val[['VAL_AUTO_NUM', 'peso_valor_norm', 'valor_quintil', 'DES_LOCAL_', 'MUNICIPIO', 'UF', 'geometry']].to_file(output_val)
print(f"      Salvo em: {output_val}")

# *** CAMADA 4: COMBINADA (ÍNDICE COMPOSTOS) ***
print("\n   CAMADA 4: Índice Composto (Tipo + Gravidade + Valor)")
gdf_combined = gdf[
    (gdf['TIPO_AUTO'].notna()) & 
    (gdf['GRAVIDADE_'].notna()) & 
    (gdf['VAL_AUTO_NUM'].notna())
].copy()

print(f"      Registros com todas 3 dimensões: {len(gdf_combined)}")

# Recalcular pesos para a combinação
tipo_counts_combined = gdf_combined['TIPO_AUTO'].value_counts()
grav_counts_combined = gdf_combined['GRAVIDADE_'].value_counts()

peso_tipo_combined = gdf_combined['TIPO_AUTO'].map(tipo_counts_combined)
peso_grav_combined = gdf_combined['GRAVIDADE_'].map(grav_counts_combined)

# Normalizar cada dimensão
norm_tipo = (peso_tipo_combined - peso_tipo_combined.min()) / (peso_tipo_combined.max() - peso_tipo_combined.min())
norm_grav = (peso_grav_combined - peso_grav_combined.min()) / (peso_grav_combined.max() - peso_grav_combined.min())
norm_val = (gdf_combined['VAL_AUTO_NUM'] - gdf_combined['VAL_AUTO_NUM'].min()) / (gdf_combined['VAL_AUTO_NUM'].max() - gdf_combined['VAL_AUTO_NUM'].min())

# Índice composto: média ponderada
# Pesos: 30% Tipo, 30% Gravidade, 40% Valor (ajuste conforme necessário)
gdf_combined['indice_risco'] = (0.3 * norm_tipo + 
                                 0.3 * norm_grav + 
                                 0.4 * norm_val) * 100

# Classificar risco
gdf_combined['classe_risco'] = pd.cut(gdf_combined['indice_risco'], 
                                       bins=[0, 20, 40, 60, 80, 100],
                                       labels=['Muito Baixo', 'Baixo', 'Médio', 'Alto', 'Muito Alto'])

# Salvar
output_combined = heat_dir / "heat_indice_composto.shp"
gdf_combined[['TIPO_AUTO', 'GRAVIDADE_', 'VAL_AUTO_NUM', 'indice_risco', 'classe_risco', 'DES_LOCAL_', 'MUNICIPIO', 'UF', 'geometry']].to_file(output_combined)
print(f"      Salvo em: {output_combined}")

# ============================================================================
# 4. ANÁLISES POR AGREGAÇÃO ESPACIAL
# ============================================================================
print("\n4. Análises agregadas por municípios:")
print("-" * 100)

# Agregação por município
# Agregação manual
print("   Agregando dados por município...")
# Agregação manual
municipios_agg = []
for municipio in gdf['MUNICIPIO'].unique():
    gdf_mun = gdf[gdf['MUNICIPIO'] == municipio]
    municipios_agg.append({
        'MUNICIPIO': municipio,
        'qtd_infraçoes': len(gdf_mun),
        'valor_total': gdf_mun['VAL_AUTO_NUM'].sum() if gdf_mun['VAL_AUTO_NUM'].notna().any() else 0,
        'valor_medio': gdf_mun['VAL_AUTO_NUM'].mean() if gdf_mun['VAL_AUTO_NUM'].notna().any() else 0,
        'valor_maximo': gdf_mun['VAL_AUTO_NUM'].max() if gdf_mun['VAL_AUTO_NUM'].notna().any() else 0,
        'geometry': gdf_mun.iloc[0]['geometry'] if len(gdf_mun) > 0 else None
    })

agg_municipio = pd.DataFrame(municipios_agg)
gdf_agg = gpd.GeoDataFrame(agg_municipio, geometry='geometry', crs='EPSG:4326')

# Centroid do município para melhor visualização
gdf_agg['geometry'] = gdf_agg['geometry'].centroid

# Normalizar para mapa de calor
gdf_agg['intensidade'] = (gdf_agg['qtd_infraçoes'] - gdf_agg['qtd_infraçoes'].min()) / (gdf_agg['qtd_infraçoes'].max() - gdf_agg['qtd_infraçoes'].min()) * 100
gdf_agg['intensidade_valor'] = (gdf_agg['valor_total'] - gdf_agg['valor_total'].min()) / (gdf_agg['valor_total'].max() - gdf_agg['valor_total'].min()) * 100

output_agg = heat_dir / "heat_municipios_agregado.shp"
gdf_agg.to_file(output_agg)
print(f"      Agregação por município: {output_agg}")
print(f"      Total de municípios: {len(gdf_agg)}")

# ============================================================================
# 5. GRIDS DE DENSIDADE (HEATMAP RASTERIZADO)
# ============================================================================
print("\n5. Criando grids de densidade para análise de calor:")
print("-" * 100)

def create_density_grid(gdf, grid_size=0.5):
    """Cria grid de densidade para heatmap"""
    bounds = gdf.total_bounds
    minx, miny, maxx, maxy = bounds
    
    # Criar grid
    x_range = np.arange(minx, maxx, grid_size)
    y_range = np.arange(miny, maxy, grid_size)
    
    cells = []
    for x in x_range:
        for y in y_range:
            cell_box = box(x, y, x + grid_size, y + grid_size)
            cells.append(cell_box)
    
    grid = gpd.GeoDataFrame(geometry=cells, crs='EPSG:4326')
    
    # Contar pontos em cada célula
    grid['count'] = grid.geometry.apply(lambda x: len(gdf[gdf.geometry.within(x)]))
    
    # Filtrar células vazias
    grid = grid[grid['count'] > 0].copy()
    
    # Normalizar intensidade
    grid['intensity'] = (grid['count'] - grid['count'].min()) / (grid['count'].max() - grid['count'].min()) * 100
    
    return grid

print("\n   Criando grid de densidade (0.5° x 0.5°)...")
grid_density = create_density_grid(gdf, grid_size=0.5)
output_grid = heat_dir / "heat_grid_density.shp"
grid_density[['count', 'intensity', 'geometry']].to_file(output_grid)
print(f"      Grid salvo em: {output_grid}")
print(f"      Células com infrações: {len(grid_density)}")

# ============================================================================
# 6. ESTATÍSTICAS FINAIS
# ============================================================================
print("\n6. Estatísticas finais para mapas de calor:")
print("-" * 100)

print(f"\n   Camadas criadas para QGIS:")
print(f"   1. heat_tipo_auto.shp - Intensidade por tipo de auto")
print(f"   2. heat_gravidade.shp - Intensidade por gravidade")
print(f"   3. heat_valor.shp - Intensidade por valor financeiro")
print(f"   4. heat_indice_composto.shp - Índice combinado (RECOMENDADO)")
print(f"   5. heat_municipios_agregado.shp - Visualização agregada por município")
print(f"   6. heat_grid_density.shp - Grid de densidade")

print(f"\n   Resumo de dados por camada:")
print(f"      - Tipo Auto: {len(gdf_tipo)} registros")
print(f"      - Gravidade: {len(gdf_grav)} registros")
print(f"      - Valor: {len(gdf_val)} registros")
print(f"      - Índice Composto: {len(gdf_combined)} registros")

# ============================================================================
# 7. EXPORTAR PARA GeoJSON (COMPATÍVEL COM MAIS FERRAMENTAS)
# ============================================================================
print("\n7. Exportando para GeoJSON (compatível com mais ferramentas):")
print("-" * 100)

gdf_combined.to_file(heat_dir / "heat_indice_composto.geojson", driver='GeoJSON')
print(f"   heat_indice_composto.geojson")

grid_density.to_file(heat_dir / "heat_grid_density.geojson", driver='GeoJSON')
print(f"   heat_grid_density.geojson")

gdf_agg.to_file(heat_dir / "heat_municipios_agregado.geojson", driver='GeoJSON')
print(f"   heat_municipios_agregado.geojson")

print("\n" + "=" * 100)
print("PREPARAÇÃO DE DADOS CONCLUÍDA")
print("=" * 100)
print(f"\nTodos os arquivos estão em: {heat_dir}")
print("\nPróximo passo: Abrir no QGIS e aplicar")
print("  - Heatmap renderer para densidade")
print("  - Symbology baseado em 'indice_risco' ou 'intensity'")
print("  - Criar animações temporais se desejar")
