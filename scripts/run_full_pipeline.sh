#!/usr/bin/env bash
set -euo pipefail

noise-sim clean-points \
  --input data/raw/Germany_Bayern_Bamberg.points.geojson \
  --output data/processed/cleaned_noise_points.geojson

noise-sim make-grid \
  --boundary data/raw/Germany_Bayern_Bamberg.areas.geojson \
  --output data/processed/cleaned_bamberg_grid.geojson

noise-sim assign-points \
  --points data/processed/cleaned_noise_points.geojson \
  --grid data/processed/cleaned_bamberg_grid.geojson \
  --output data/processed/grid_summary.csv

# then call your simulation commands (static & adaptive)
noise-sim simulate-static \
  --areas data/processed/cleaned_bamberg_grid.geojson \
  --num-users 500 \
  --reward 1.0

noise-sim simulate-ucb \
  --areas data/processed/cleaned_bamberg_grid.geojson \
  --num-users 500 \
  --reward 1.0
