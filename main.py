from __future__ import annotations

import matplotlib.pyplot as plt

from src import config
from src import loader
from src import preprocessing
from src.simulation.static_simulation import run as run_static


def run():
    # Step 1: Load data
    print("\nLoading GeoJSON files...")
    areas, points, _ = loader.load_data(
        config.AREA_PATH, config.POINT_PATH, config.TRACK_PATH
    )

    # Step 2: Inspect data structure
    print("\n--- AREA COLUMNS ---")
    print(areas.columns.tolist())
    print(areas.head())

    print("\n--- POINT COLUMNS ---")
    print(points.columns.tolist())
    print(points.head())

    # Step 3: Clean noise points
    points_cleaned = preprocessing.clean_points(points, db_col="noise_level")
    print(f"\nCleaned noise points: {len(points_cleaned)}")

    # Step 4: Apply CRS consistency
    areas, points_cleaned = preprocessing.apply_crs(
        [areas, points_cleaned], config.TARGET_CRS
    )

    # Step 5: Assign points to areas and count measurements
    enriched_areas = preprocessing.assign_points_to_areas(
        points_cleaned, areas
    )
    print("\nAssigned measure counts per area:")
    print(enriched_areas[["measure_count"]].describe())

    # Step 6: Plot data for inspection
    print("\nPlotting raw data...")

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
    # Fix geometries before saving (ensures compatibility)
    enriched_areas["geometry"] = enriched_areas["geometry"].buffer(0)
    enriched_areas.to_file(
        "output/cleaned_bamberg_areas.geojson", driver="GeoJSON"
    )
    enriched_areas.drop(columns="geometry").to_csv(
        "output/grid_summary.csv", index=False
    )
    print("\nSaved cleaned data to output")

    # --- Static Incentive Simulation ---
    print("\nRunning static incentive simulation...")
    sim_results = run_static(
        areas=enriched_areas,
        num_users=500,
        reward_per_submission=1.0,
        random_seed=42,
    )

    # Print simulation outputs
    print("\nStatic Simulation Results:")
    print("Total payout: €", sim_results["total_payout"])
    print("New submissions summary:")
    print(sim_results["new_submissions"].describe())

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
