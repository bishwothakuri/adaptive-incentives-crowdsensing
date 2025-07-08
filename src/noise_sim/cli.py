from __future__ import annotations

import click
import geopandas as gpd

from .config import CLEANED_AREAS_PATH
from .config import GRID_CELL_SIZE_METERS
from .config import GRID_PATH
from .config import GRID_SUMMARY_CSV
from .config import METRIC_CRS_EPSG
from .config import RAW_AREA_PATH
from .config import RAW_POINT_PATH
from .preprocessing import assign_points_to_areas
from .preprocessing import clean_points
from .preprocessing import create_and_save_grid


@click.group()
def cli():
    """NoisePlanet Simulation Toolkit"""
    pass


@cli.command("clean-points")
@click.option(
    "--input",
    "-i",
    type=click.Path(exists=True, dir_okay=False),
    default=RAW_POINT_PATH,
    help="Raw GeoJSON of noise points",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(dir_okay=False),
    default=CLEANED_AREAS_PATH.parent / "cleaned_noise_points.geojson",
    help="Output path for cleaned points",
)
@click.option(
    "--min-db", type=int, default=30, help="Minimum noise level (dB)"
)
@click.option(
    "--max-db", type=int, default=120, help="Maximum noise level (dB)"
)
@click.option(
    "--max-accuracy", type=float, default=15.0, help="Max GPS accuracy (m)"
)
def cmd_clean_points(input, output, min_db, max_db, max_accuracy):
    """Clean raw noise points by dB range and accuracy."""
    click.echo(f"Loading raw points from {input}")
    gdf = gpd.read_file(input)
    cleaned = clean_points(
        gdf,
        db_col="noise_level",
        min_db=min_db,
        max_db=max_db,
        max_accuracy=max_accuracy,
    )
    cleaned.to_file(output, driver="GeoJSON")
    click.echo(f"Cleaned points written to {output}")


@cli.command("make-grid")
@click.option(
    "--boundary",
    "-b",
    type=click.Path(exists=True, dir_okay=False),
    default=RAW_AREA_PATH,
    help="Raw GeoJSON of city boundary",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(dir_okay=False),
    default=GRID_PATH,
    help="Output path for the generated grid",
)
@click.option(
    "--cell-size",
    "-s",
    type=int,
    default=GRID_CELL_SIZE_METERS,
    help="Grid cell size (metres)",
)
@click.option(
    "--metric-crs",
    "-m",
    default=METRIC_CRS_EPSG,
    help="EPSG code for metric CRS",
)
def cmd_make_grid(boundary, output, cell_size, metric_crs):
    """Generate a square grid clipped to the city boundary."""
    click.echo(f"Reading boundary from {boundary}")
    create_and_save_grid(
        boundary_fp=boundary,
        output_fp=output,
        cell_size=cell_size,
        metric_epsg=metric_crs,
    )
    click.echo(f"Grid saved to {output}")


@cli.command("assign-points")
@click.option(
    "--points",
    "-p",
    type=click.Path(exists=True, dir_okay=False),
    default=CLEANED_AREAS_PATH.parent / "cleaned_noise_points.geojson",
    help="Cleaned noise points GeoJSON",
)
@click.option(
    "--grid",
    "-g",
    type=click.Path(exists=True, dir_okay=False),
    default=GRID_PATH,
    help="Grid GeoJSON",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(dir_okay=False),
    default=GRID_SUMMARY_CSV,
    help="CSV file for grid summary with measure_count",
)
def cmd_assign(points, grid, output):
    """Count points per grid cell and save summary CSV."""
    click.echo(f"Loading cleaned points from {points}")
    gdf_pts = gpd.read_file(points)
    click.echo(f"Loading grid from {grid}")
    gdf_grid = gpd.read_file(grid)
    click.echo("Assigning points to grid cells...")
    enriched = assign_points_to_areas(gdf_pts, gdf_grid)
    enriched.to_file(grid, driver="GeoJSON")  # update grid with measure_count
    # Also save a CSV summary
    enriched[["measure_count"]].to_csv(output)
    click.echo(f"Updated grid written to {grid}")
    click.echo(f"Grid summary CSV written to {output}")


if __name__ == "__main__":
    cli()
