from pathlib import Path
import argparse

import pandas as pd
import geopandas as gpd
from shapely import wkt
from shapely.geometry import Point


CSV_PATTERN = "auto_infracao_ano_*.csv"
LAT_COL = "NUM_LATITUDE_AUTO"
LON_COL = "NUM_LONGITUDE_AUTO"
DATE_COLS = ["DT_FATO_INFRACIONAL", "DT_INICIO_ATO_INEQUIVOCO", "DT_LANCAMENTO"]
WKT_COLS = ["DS_WKT", "WKT_GE_AREA_AUTUADA"]
LON_COL = "NUM_LONGITUDE_AUTO"
WKT_COLS = ["DS_WKT", "WKT_GE_AREA_AUTUADA"]


def parse_coordinate(value):
    if pd.isna(value):
        return None
    text = str(value).strip()
    if text == "":
        return None
    text = text.replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return None


def resolve_date_column(df: pd.DataFrame, selected_column=None):
    if selected_column and selected_column in df.columns:
        return selected_column
    for col in DATE_COLS:
        if col in df.columns:
            return col
    return None


def filter_recent_years(df: pd.DataFrame, years: int, selected_column=None):
    date_col = resolve_date_column(df, selected_column)
    if not date_col:
        print("     nenhum campo de data encontrado; mantendo todos os registros")
        return df

    parsed = pd.to_datetime(df[date_col], errors="coerce", dayfirst=False)
    threshold = pd.Timestamp.now() - pd.DateOffset(years=years)
    date_mask = parsed >= threshold
    kept = date_mask.sum()
    total = len(df)
    print(f"     filtrando últimos {years} anos pela coluna {date_col}: {kept} de {total} registros mantidos")
    df = df.loc[date_mask].copy()
    df["parsed_date"] = parsed.loc[date_mask]
    return df


def load_csv_file(path: Path) -> pd.DataFrame:
    df = pd.read_csv(
        path,
        sep=";",
        dtype=str,
        encoding="utf-8",
        low_memory=False,
        keep_default_na=False,
    )
    df["source_file"] = path.name
    print_read_confirmation(path, df)
    return df


def print_read_confirmation(path: Path, df: pd.DataFrame):
    num_rows = len(df)
    num_cols = len(df.columns)
    print(f"  -> {path.name}: {num_rows} registros lidos, {num_cols} colunas")

    cols_preview = ", ".join(df.columns[:6].tolist())
    if num_cols > 6:
        cols_preview += ", ..."
    print(f"     colunas: {cols_preview}")

    if LAT_COL in df.columns and LON_COL in df.columns:
        valid_latlon = df[LAT_COL].notna() & df[LON_COL].notna()
        print(f"     lat/lon presentes em {valid_latlon.sum()} registros")
    else:
        print("     colunas de coordenadas não encontradas no arquivo")


def build_geodataframe(df: pd.DataFrame) -> gpd.GeoDataFrame:
    df = df.copy()

    df["longitude"] = df[LON_COL].apply(parse_coordinate) if LON_COL in df.columns else None
    df["latitude"] = df[LAT_COL].apply(parse_coordinate) if LAT_COL in df.columns else None

    has_points = df["longitude"].notna() & df["latitude"].notna()
    if has_points.any():
        df.loc[has_points, "geometry"] = gpd.points_from_xy(
            df.loc[has_points, "longitude"],
            df.loc[has_points, "latitude"],
            crs="EPSG:4326",
        )
    else:
        df["geometry"] = None

    missing_geometry = df["geometry"].isna()
    if missing_geometry.any():
        for wkt_col in WKT_COLS:
            if wkt_col not in df.columns:
                continue
            valid = missing_geometry & df[wkt_col].notna() & (df[wkt_col].str.strip() != "")
            if valid.any():
                df.loc[valid, "geometry"] = df.loc[valid, wkt_col].apply(_parse_wkt)
                missing_geometry = df["geometry"].isna()
            if not missing_geometry.any():
                break

    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")
    return gdf


def _parse_wkt(value: str):
    try:
        return wkt.loads(value)
    except Exception:
        return None


def build_point_geodataframe(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    points = []
    for _, row in gdf.iterrows():
        point_geom = None
        if pd.notna(row.get("longitude")) and pd.notna(row.get("latitude")):
            point_geom = Point(row["longitude"], row["latitude"])
        else:
            geom = row.get("geometry")
            if geom is not None:
                if geom.geom_type == "Point":
                    point_geom = geom
                else:
                    point_geom = geom.centroid
        points.append(point_geom)

    point_gdf = gdf.copy()
    point_gdf["geometry"] = points
    return gpd.GeoDataFrame(point_gdf, geometry="geometry", crs="EPSG:4326")


def validate_geometries(gdf: gpd.GeoDataFrame) -> dict:
    valid_mask = gdf["geometry"].notna()
    invalid_mask = ~valid_mask
    return {
        "total": len(gdf),
        "valid": valid_mask.sum(),
        "invalid": invalid_mask.sum(),
        "valid_mask": valid_mask,
        "invalid_mask": invalid_mask,
    }


def process_directory(data_dir: Path, years: int, date_column=None) -> gpd.GeoDataFrame:
    csv_files = sorted(data_dir.glob(CSV_PATTERN))
    if not csv_files:
        raise FileNotFoundError(f"Nenhum arquivo CSV encontrado em: {data_dir}")

    all_gdfs = []
    for csv_file in csv_files:
        print(f"Lendo: {csv_file.name}")
        df = load_csv_file(csv_file)
        df = filter_recent_years(df, years, date_column)
        gdf = build_geodataframe(df)
        print_geometry_summary(csv_file.name, gdf)
        all_gdfs.append(gdf)

    result = pd.concat(all_gdfs, ignore_index=True)
    result = gpd.GeoDataFrame(result, geometry="geometry", crs="EPSG:4326")
    return result


def print_geometry_summary(source_name: str, gdf: gpd.GeoDataFrame):
    stats = validate_geometries(gdf)
    print(f"     geometria válida em {stats['valid']} de {stats['total']} registros")
    if stats["invalid"] > 0:
        print(f"     registros inválidos: {stats['invalid']}")
        invalid_sample = gdf.loc[stats["invalid_mask"], ["source_file", LAT_COL, LON_COL] + [col for col in WKT_COLS if col in gdf.columns]].head(3)
        print("     exemplo de registros inválidos:")
        for idx, row in invalid_sample.iterrows():
            print(f"       - {row['source_file']}: {LAT_COL}={row.get(LAT_COL)} {LON_COL}={row.get(LON_COL)} WKT={row.get('DS_WKT') or row.get('WKT_GE_AREA_AUTUADA')}")
    if stats["valid"] > 0:
        sample = gdf.loc[stats["valid_mask"], ["source_file", "longitude", "latitude", "geometry"]].head(3)
        print("     exemplo de geometria válida:")
        for idx, row in sample.iterrows():
            print(f"       - {row['source_file']}: lon={row['longitude']} lat={row['latitude']} geom={row['geometry']}")


def save_output(gdf: gpd.GeoDataFrame, output_dir: Path, output_format: str):
    output_dir.mkdir(parents=True, exist_ok=True)
    output_format = output_format.lower()
    stats = validate_geometries(gdf)
    valid_gdf = gdf.loc[stats["valid_mask"]].copy()
    point_gdf = build_point_geodataframe(valid_gdf)

    if output_format == "geojson":
        output_path = output_dir / "auto_infracao_coords_valid.geojson"
        valid_gdf.to_file(output_path, driver="GeoJSON")
        point_path = output_dir / "auto_infracao_points_complete.geojson"
        point_gdf.to_file(point_path, driver="GeoJSON")
    elif output_format == "shp":
        output_path = output_dir / "auto_infracao_points_complete.shp"
        point_gdf.to_file(output_path)
        point_path = output_path
    elif output_format == "csv":
        output_path = output_dir / "auto_infracao_coords_valid.csv"
        out_df = valid_gdf.drop(columns="geometry")
        out_df.to_csv(output_path, index=False)
        point_path = output_dir / "auto_infracao_points_complete.csv"
        point_df = point_gdf.copy()
        point_df["geometry"] = point_df["geometry"].apply(lambda geom: geom.wkt if geom is not None else "")
        point_df.to_csv(point_path, index=False)
    else:
        raise ValueError("Formato inválido. Use geojson, shp ou csv.")

    print(f"Salvo em: {output_path}")
    print(f"Arquivo de pontos completo salvo em: {point_path}")
    if stats["invalid"] > 0:
        invalid_path = output_dir / "invalid_auto_infracao_rows.csv"
        invalid_df = gdf.loc[stats["invalid_mask"]].drop(columns="geometry")
        invalid_df.to_csv(invalid_path, index=False)
        print(f"Registros inválidos salvos em: {invalid_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Extrai coordenadas geográficas de autos de infração CSV e grava arquivo espacial ou CSV.",
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Pasta onde estão os arquivos auto_infracao_ano_*.csv",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "output",
        help="Pasta de saída para os arquivos gerados.",
    )
    parser.add_argument(
        "--format",
        choices=["geojson", "shp", "csv"],
        default="geojson",
        help="Formato de saída.",
    )
    parser.add_argument(
        "--years",
        type=int,
        default=15,
        help="Número de anos recentes a incluir na extração.",
    )
    parser.add_argument(
        "--date-column",
        type=str,
        default=None,
        help="Coluna de data a usar para o filtro de anos.",
    )
    args = parser.parse_args()

    gdf = process_directory(args.data_dir, args.years, args.date_column)
    valid_count = gdf["geometry"].notna().sum()
    total_count = len(gdf)
    print(f"Registros lidos: {total_count}")
    print(f"Registros com geometria válida: {valid_count}")

    if total_count > 0:
        print("\nAmostra de validação (primeiras 5 linhas):")
        sample_columns = ["source_file", "longitude", "latitude", "geometry"]
        sample_columns = [col for col in sample_columns if col in gdf.columns]
        print(gdf[sample_columns].head(5).to_string(index=False))

    save_output(gdf, args.output_dir, args.format)


if __name__ == "__main__":
    main()
