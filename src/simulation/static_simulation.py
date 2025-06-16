from __future__ import annotations

import numpy as np
import pandas as pd


def run(areas, num_users=500, reward_per_submission=1.0, random_seed=None):
    """
    Static incentive simulation:
    Each synthetic user picks one grid cell uniformly at random
    and receives a fixed monetary reward.

    Parameters:
    -----------
    areas : GeoDataFrame
        Must contain a 'measure_count' column with the baseline counts.
    num_users : int
        Number of synthetic participants to simulate.
    reward_per_submission : float
        Flat reward (in €) paid per submission.
    random_seed : int, optional
        Seed for reproducible random draws.

    Returns:
    --------
    results : dict
        {
          'initial_counts': pd.Series,   # original measure_count per cell
          'new_submissions': pd.Series,  # how many new picks each cell got
          'final_counts': pd.Series,     # initial + new submissions
          'total_payout': float          # total € paid out
                                          (num_users * reward)
        }
    """
    if random_seed is not None:
        np.random.seed(random_seed)

    # Record the baseline coverage
    initial_counts = areas["measure_count"].copy()

    # List of cell indices
    cells = list(areas.index)

    # Simulate each user choosing a cell uniformly at random
    choices = np.random.choice(cells, size=num_users)

    # Count how many times each cell was chosen
    new_submissions = (
        pd.Series(choices).value_counts().reindex(cells, fill_value=0)
    )

    # Compute the updated coverage
    final_counts = initial_counts.add(new_submissions, fill_value=0).astype(
        int
    )

    # Total cost of rewards
    total_payout = num_users * reward_per_submission

    return {
        "initial_counts": initial_counts,
        "new_submissions": new_submissions,
        "final_counts": final_counts,
        "total_payout": total_payout,
    }
