from __future__ import annotations

import geopandas as gpd


def load_data(area_fp: str, point_fp: str, track_fp: str = None):
    """
    Loads Noise Planet data (areas, points, optionally tracks)
    from GeoJSON files.

    Parameters:
        area_fp (str): File path to grid area GeoJSON.
        point_fp (str): File path to noise points GeoJSON.
        track_fp (str, optional): File path to movement tracks GeoJSON.

    Returns:
        tuple: (GeoDataFrame of areas, GeoDataFrame of points,
        [GeoDataFrame of tracks or None])
    """
    print(" Loading GeoJSON files...")

    gdf_areas = gpd.read_file(area_fp)
    gdf_points = gpd.read_file(point_fp)

    gdf_tracks = gpd.read_file(track_fp) if track_fp else None

    print(
        f" Loaded {len(gdf_areas)} areas, {len(gdf_points)} points"
        + (f", {len(gdf_tracks)} tracks" if gdf_tracks is not None else "")
    )

    return gdf_areas, gdf_points, gdf_tracks
