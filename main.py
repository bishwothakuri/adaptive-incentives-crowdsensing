from __future__ import annotations

import logging

import matplotlib.pyplot as plt

from src import config
from src import loader
from src import preprocessing
from src.simulation.static_simulation import run as run_static
from src.utils.logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


def run():
    # Step 1: Load data
    logger.info("Loading GeoJSON files...")
    areas, points, _ = loader.load_data(
        config.AREA_PATH, config.POINT_PATH, config.TRACK_PATH
    )

    # Step 2: Inspect data structure
    logger.info("--- AREA COLUMNS ---")
    logger.info(areas.columns.tolist())
    logger.info(areas.head())

    logger.info("--- POINT COLUMNS ---")
    logger.info(points.columns.tolist())
    logger.info(points.head())

    # Step 3: Clean noise points
    points_cleaned = preprocessing.clean_points(points, db_col="noise_level")
    logger.info(f"Cleaned noise points: {len(points_cleaned)}")

    # Step 4: Apply CRS consistency
    areas, points_cleaned = preprocessing.apply_crs(
        [areas, points_cleaned], config.TARGET_CRS
    )

    # Step 5: Assign points to areas and count measurements
    enriched_areas = preprocessing.assign_points_to_areas(
        points_cleaned, areas
    )
    logger.info("Assigned measure counts per area:")
    logger.info(enriched_areas[["measure_count"]].describe())

    # Step 6: Plot data for inspection
    logger.info("Plotting raw data...")

    areas.plot(edgecolor="black", facecolor="none")
    plt.title("Grid Areas (Raw)")
    plt.axis("off")
    plt.show()

    points_cleaned.plot(markersize=1, color="red")
    plt.title("Cleaned Noise Points")
    plt.axis("off")
    plt.show()

    enriched_areas.plot(column="measure_count", cmap="OrRd", legend=True)
    plt.title("Noise Measurement Count per Area")
    plt.axis("off")
    plt.show()

    # Step 7: Save cleaned and enriched areas
    enriched_areas["geometry"] = enriched_areas["geometry"].buffer(0)
    enriched_areas.to_file(
        "output/cleaned_bamberg_areas.geojson", driver="GeoJSON"
    )
    enriched_areas.drop(columns="geometry").to_csv(
        "output/grid_summary.csv", index=False
    )
    logger.info("Saved cleaned data to output")

    # --- Static Incentive Simulation ---
    logger.info("Running static incentive simulation...")
    sim_results = run_static(
        areas=enriched_areas,
        num_users=500,
        reward_per_submission=1.0,
        random_seed=42,
    )

    # Print simulation outputs
    logger.info("Static Simulation Results:")
    logger.info(f"Total payout: € {sim_results['total_payout']}")
    logger.info("New submissions summary:")
    logger.info(sim_results["new_submissions"].describe())

    # Plot new submissions per cell
    plt.figure(figsize=(10, 4))
    sim_results["new_submissions"].sort_values().plot.bar()
    plt.title("Static Scheme: New Submissions per Grid Cell")
    plt.xlabel("Grid Cell Index")
    plt.ylabel("Number of New Submissions")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    run()
