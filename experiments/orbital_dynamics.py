import numpy as np
import pandas as pd

from scythe.base import ExperimentInputSpec, ExperimentOutputSpec
from scythe.registry import ExperimentRegistry


class OrbitalDynamicsInputs(ExperimentInputSpec):
    semi_major_axis: float  # in km
    eccentricity: float  # dimensionless (0-1)
    inclination: float  # in degrees


class OrbitalDynamicsOutputs(ExperimentOutputSpec):
    orbital_period_hours: float
    orbital_velocity_km_s: float
    apogee_distance_km: float
    perigee_distance_km: float


@ExperimentRegistry.Register()
def simulate_orbital_dynamics(
    input_spec: OrbitalDynamicsInputs,
) -> OrbitalDynamicsOutputs:
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

    experiment_metrics = pd.DataFrame(
        data={
            "simulation_runtime_ms": [np.random.normal(50, 5)],
            "energy_used_joules": [np.random.normal(200, 20)],
            "memory_used_mb": [np.random.normal(15, 2)],
            "cpu_time_ms": [np.random.normal(30, 3)],
        },
    )
    experiment_metrics.index = input_spec.make_multiindex(
        n_rows=len(experiment_metrics)
    )

    results = OrbitalDynamicsOutputs(
        dataframes={"metrics": experiment_metrics},
        orbital_period_hours=orbital_period,
        orbital_velocity_km_s=orbital_velocity,
        apogee_distance_km=apogee_distance,
        perigee_distance_km=perigee_distance,
    )
    return results
