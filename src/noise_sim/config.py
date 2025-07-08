from __future__ import annotations

from pathlib import Path

# ─── Raw data paths ──────────────────────────────
RAW_DIR = Path("data/raw")
RAW_AREA_PATH = RAW_DIR / "Germany_Bayern_Bamberg.areas.geojson"
RAW_POINT_PATH = RAW_DIR / "Germany_Bayern_Bamberg.points.geojson"
RAW_TRACK_PATH = RAW_DIR / "Germany_Bayern_Bamberg.tracks.geojson"

# ─── Processed data paths ─────────────────────────────
PROCESSED_DIR = Path("data/processed")
CLEANED_AREAS_PATH = PROCESSED_DIR / "cleaned_bamberg_areas.geojson"
GRID_PATH = PROCESSED_DIR / "cleaned_bamberg_grid.geojson"
GRID_SUMMARY_CSV = PROCESSED_DIR / "grid_summary.csv"

# ─── Grid settings ────────────────────────────────────
GRID_CELL_SIZE_METERS = 100  # 100 m × 100 m
METRIC_CRS_EPSG = 25832  # UTM zone 32N (meters)
WGS84_CRS = "EPSG:4326"  # WGS84 lat/lon

# ─── Simulation settings ───────────────────────────────
DEFAULT_PARTICIPANTS = 500
