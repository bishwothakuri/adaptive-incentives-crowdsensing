from __future__ import annotations

import geopandas as gpd
import numpy as np
from shapely.geometry import box


def clean_points(
    gdf_points,
    db_col="noise_level",
    min_db=30,
    max_db=120,
    max_accuracy=15,
):
    """
    Filters the noise points for realistic values.
    """
    gdf_points = gdf_points[
        (gdf_points[db_col] >= min_db) & (gdf_points[db_col] <= max_db)
    ]

    if "accuracy" in gdf_points.columns:
        gdf_points = gdf_points[gdf_points["accuracy"] <= max_accuracy]

    return gdf_points


def apply_crs(gdf_list, target_crs="EPSG:4326"):
    """
    Ensures all GeoDataFrames are using the same CRS.
    """
    return [gdf.to_crs(target_crs) for gdf in gdf_list]


def assign_points_to_areas(gdf_points, gdf_areas):
    """
    Assigns noise points to spatial areas using a spatial join and counts
    measures per area.
    """
    # Spatial join: which area each point falls into
    joined = gpd.sjoin(
        gdf_points, gdf_areas, how="inner", predicate="intersects"
    )

    # Count number of points per area
    measure_counts = (
        joined.groupby("index_right").size().rename("measure_count")
    )

    # Add measure_count to original areas GeoDataFrame
    gdf_areas["measure_count"] = measure_counts
    gdf_areas["measure_count"] = (
        gdf_areas["measure_count"].fillna(0).astype(int)
    )

    return gdf_areas


def make_square_grid(
    boundary_gdf: gpd.GeoDataFrame, cell_size: int = 100
) -> gpd.GeoDataFrame:
    """
    Build a square grid (in metres) over the boundary polygon.
    Returns only the cells that intersect the boundary.
    """
    # 1. Get the bounding box of the city in metric CRS
    minx, miny, maxx, maxy = boundary_gdf.total_bounds

    # 2. Create grid cell corners at 'cell_size' intervals
    xs = np.arange(minx, maxx + cell_size, cell_size)
    ys = np.arange(miny, maxy + cell_size, cell_size)

    # 3. Build square polygons for each cell
    cells = [
        box(x, y, x + cell_size, y + cell_size)
        for x in xs[:-1]
        for y in ys[:-1]
    ]

    # 4. Create a GeoDataFrame and clip to the city boundary
    grid = gpd.GeoDataFrame({"geometry": cells}, crs=boundary_gdf.crs)
    grid = gpd.overlay(grid, boundary_gdf, how="intersection")
    return grid


def create_and_save_grid(
    boundary_fp: str,
    output_fp: str,
    cell_size: int = 100,
    metric_epsg: int = 25832,
) -> None:
    """
    Load a boundary GeoJSON, generate a square grid in a metric CRS,
    reproject to WGS84, and save it to output_fp.
    """
    # 1. Read boundary and reproject to a metric CRS (e.g. UTM zone 32N)
    boundary = gpd.read_file(boundary_fp).to_crs(epsg=metric_epsg)

    # 2. Build and clip the grid
    grid = make_square_grid(boundary, cell_size)

    # 3. Reproject back to lat/lon and write as GeoJSON
    grid.to_crs(epsg=4326).to_file(output_fp, driver="GeoJSON")
