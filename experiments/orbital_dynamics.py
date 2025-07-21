import numpy as np
import pandas as pd

from scythe.base import ExperimentInputSpec, ExperimentOutputSpec
from scythe.registry import ExperimentRegistry
from scythe.utils.results import make_onerow_multiindex_from_dict


class OrbitalDynamicsInputs(ExperimentInputSpec):
    semi_major_axis: float  # in km
    eccentricity: float  # dimensionless (0-1)
    inclination: float  # in degrees


@ExperimentRegistry.Register
def simulate_orbital_dynamics(
    input_spec: OrbitalDynamicsInputs,
) -> ExperimentOutputSpec:
    # Gravitational constant for Earth (km³/s²)
    mu_earth = 398600.4418

    # Calculate orbital period using Kepler's Third Law
    orbital_period = (
        2 * np.pi * np.sqrt((input_spec.semi_major_axis**3) / mu_earth) / 3600
    )  # in hours

    # Calculate orbital velocity at perigee
    perigee_distance = input_spec.semi_major_axis * (1 - input_spec.eccentricity)
    orbital_velocity = np.sqrt(
        mu_earth * (2 / perigee_distance - 1 / input_spec.semi_major_axis)
    )  # km/s

    # Calculate apogee distance
    apogee_distance = input_spec.semi_major_axis * (1 + input_spec.eccentricity)

    # Add some realistic noise to the calculations
    orbital_period += np.random.normal(0, 0.1)
    orbital_velocity += np.random.normal(0, 0.01)

    index_data = input_spec.model_dump(mode="json")
    multi_index = make_onerow_multiindex_from_dict(index_data)
    results_df = pd.DataFrame(
        data={
            "orbital_period_hours": [orbital_period],
            "orbital_velocity_km_s": [orbital_velocity],
            "apogee_distance_km": [apogee_distance],
            "perigee_distance_km": [perigee_distance],
        },
        index=multi_index,
    )

    experiment_metrics = pd.DataFrame(
        data={
            "simulation_runtime_ms": [np.random.normal(50, 5)],
            "energy_used_joules": [np.random.normal(200, 20)],
            "memory_used_mb": [np.random.normal(15, 2)],
            "cpu_time_ms": [np.random.normal(30, 3)],
        },
        index=multi_index,
    )

    return ExperimentOutputSpec(
        dataframes={
            "orbital_parameters": results_df,
            "metrics": experiment_metrics,
        },
    )
