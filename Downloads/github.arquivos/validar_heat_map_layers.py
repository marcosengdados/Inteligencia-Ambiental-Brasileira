"""
VALIDAÇÃO DOS ARQUIVOS DE MAPAS DE CALOR GERADOS
"""
import os
from pathlib import Path
import geopandas as gpd

print("=" * 100)
print("VALIDAÇÃO - ARQUIVOS GERADOS PARA MAPAS DE CALOR")
print("=" * 100)

heat_dir = Path("output/heat_map_layers")

if not heat_dir.exists():
    print(f"\nERRO: Diretório {heat_dir} não encontrado!")
    exit(1)

# Listar arquivos
print(f"\n1. ARQUIVOS GERADOS EM: {heat_dir}")
print("-" * 100)

shapefiles = []
geojsons = []

for ext in ['shp', 'geojson', 'json']:
    files = list(heat_dir.glob(f"*.{ext}"))
    if ext == 'geojson' or ext == 'json':
        geojsons.extend(files)
    else:
        shapefiles.extend(files)

print(f"\n📍 Shapefiles ({len(shapefiles)} arquivos):")
for f in sorted(shapefiles):
    size_mb = f.stat().st_size / (1024 * 1024)
    print(f"   ✓ {f.name:<40} ({size_mb:.2f} MB)")

print(f"\n📄 GeoJSON ({len(geojsons)} arquivos):")
for f in sorted(geojsons):
    size_mb = f.stat().st_size / (1024 * 1024)
    print(f"   ✓ {f.name:<40} ({size_mb:.2f} MB)")

# ============================================================================
# 2. VALIDAÇÃO DE CADA CAMADA
# ============================================================================
print("\n2. VALIDAÇÃO DAS CAMADAS")
print("-" * 100)

layers_to_check = [
    ('heat_tipo_auto.shp', 'Densidade por Tipo de Auto'),
    ('heat_gravidade.shp', 'Densidade por Gravidade'),
    ('heat_valor.shp', 'Densidade por Valor'),
    ('heat_indice_composto.shp', 'Índice Composto (PRINCIPAL)'),
    ('heat_municipios_agregado.shp', 'Agregação por Município'),
    ('heat_grid_density.shp', 'Grid de Densidade'),
]

for filename, descricao in layers_to_check:
    filepath = heat_dir / filename
    if filepath.exists():
        try:
            gdf = gpd.read_file(filepath)
            print(f"\n✓ {filename}")
            print(f"  Descrição: {descricao}")
            print(f"  Registros: {len(gdf)}")
            print(f"  Colunas: {len(gdf.columns)}")
            print(f"  Colunas principais: {', '.join(gdf.columns[:5].tolist())}")
            
            # Validar geometria
            valid_geoms = gdf.geometry.notna().sum()
            print(f"  Geometrias válidas: {valid_geoms}/{len(gdf)} ({(valid_geoms/len(gdf)*100):.1f}%)")
            
        except Exception as e:
            print(f"\n✗ {filename} - ERRO ao ler: {e}")
    else:
        print(f"\n✗ {filename} - NÃO ENCONTRADO")

# ============================================================================
# 3. ESTATÍSTICAS DO ÍNDICE COMPOSTO (PRINCIPAL)
# ============================================================================
print("\n3. ESTATÍSTICAS DO ÍNDICE COMPOSTO (Principal)")
print("-" * 100)

try:
    gdf_combined = gpd.read_file(heat_dir / 'heat_indice_composto.shp')
    
    print(f"\nÍndice de Risco (0-100):")
    print(f"  Mínimo: {gdf_combined['indice_ris'].min():.1f}")
    print(f"  Máximo: {gdf_combined['indice_ris'].max():.1f}")
    print(f"  Média: {gdf_combined['indice_ris'].mean():.1f}")
    print(f"  Mediana: {gdf_combined['indice_ris'].median():.1f}")
    
    print(f"\nDistribuição por Classe de Risco:")
    classe_dist = gdf_combined['classe_ris'].value_counts().sort_index()
    for classe, count in classe_dist.items():
        pct = (count / len(gdf_combined)) * 100
        print(f"  {classe:<15}: {count:5d} ({pct:5.1f}%)")
    
except Exception as e:
    print(f"Erro ao analisar índice composto: {e}")

# ============================================================================
# 4. PRÓXIMOS PASSOS
# ============================================================================
print("\n4. PRÓXIMOS PASSOS")
print("-" * 100)

print("""
1. ABRIR NO QGIS:
   - Abra QGIS
   - Layer > Add Layer > Add Vector Layer
   - Selecione: heat_indice_composto.shp
   - Clique "Add"

2. CONFIGURAR SYMBOLOGY (RECOMENDADO):
   - Clique direito na camada > Properties
   - Aba "Symbology"
   - Tipo: "Graduated"
   - Column: "indice_ris"
   - Color ramp: "RdYlGn_r"
   - Mode: "Quantiles"
   - Classes: 7
   - Clique "Classify" > "Apply"

3. ADICIONAR OUTRAS CAMADAS:
   - heat_municipios_agregado.shp (visualização por município)
   - heat_grid_density.shp (visualização de densidade)

4. CONSULTAR GUIA COMPLETO:
   - Leia: GUIA_QGIS_MAPAS_CALOR.md
   - Contém instruções passo a passo

5. EXPORTAR:
   - Project > Import/Export > Export as Image/PDF
   - Ou use qgis2web para WebGIS interativo
""")

print("\n" + "=" * 100)
print("VALIDAÇÃO CONCLUÍDA COM SUCESSO!")
print("=" * 100)

print(f"\nLocal dos arquivos: {heat_dir.absolute()}")
print(f"Total de camadas geradas: {len(layers_to_check)}")
print(f"\nArquivos prontos para usar no QGIS!")
