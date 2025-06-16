from __future__ import annotations

import geopandas as gpd


def clean_points(
    gdf_points,
    db_col="noise_level",  # default now points to correct column
    min_db=30,
    max_db=120,
    max_accuracy=15,
):
    """
    Filters the noise points for realistic values.

    Parameters:
        gdf_points (GeoDataFrame): Raw noise point data.
        db_col (str): Column name that holds the
        noise level (e.g., 'noise_level').
        min_db (int): Minimum acceptable noise level in dB.
        max_db (int): Maximum acceptable noise level in dB.
        max_accuracy (float): Maximum acceptable GPS accuracy
        in meters (if column exists).

    Returns:
        GeoDataFrame: Cleaned noise points.
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

    Parameters:
        gdf_list (list): List of GeoDataFrames.
        target_crs (str): CRS to apply (default is WGS84).

    Returns:
        list: GeoDataFrames with updated CRS.
    """
    return [gdf.to_crs(target_crs) for gdf in gdf_list]


def assign_points_to_areas(gdf_points, gdf_areas):
    """
    Assigns noise points to spatial areas using a spatial join and counts
    measures per area.

    Parameters:
        gdf_points (GeoDataFrame): Cleaned noise points.
        gdf_areas (GeoDataFrame): Grid areas.

    Returns:
        GeoDataFrame: Enriched grid areas with a new 'measure_count' column.
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
