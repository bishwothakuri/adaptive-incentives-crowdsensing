## Data Cleaning (2024-06-17)

- Input: Raw GeoJSON points (1336)
- Filters: noise_level 30–120 dB, GPS accuracy ≤ 15 m
- Output: 950 points kept
- Rationale: Remove errors/outliers, increase trust
- Code reference: main.py: lines 10-20

## Grid Mapping

- Grid cells: 26
- Cell coverage:
  - Min: 0 readings (Cell 8)
  - Max: 169 readings (Cell 12)
  - Mean: 36.5
- Plot: [See Fig 1: grid_coverage.png]

## Static Incentive Simulation

- Synthetic users: 500
- Payout: €1 per submission
- Results: Cell picks, mean, min, max
- Screenshot: [See Fig 2: static_results.png]
