import numpy as np
import pandas as pd

from scythe.base import ExperimentInputSpec, ExperimentOutputSpec
from scythe.registry import ExperimentRegistry
from scythe.utils.results import make_onerow_multiindex_from_dict


class LifespanExperimentInputs(ExperimentInputSpec):
    age: int
    weight: float


@ExperimentRegistry.Register()
def simulate_lifespan(input_spec: LifespanExperimentInputs) -> ExperimentOutputSpec:
    simulated_lifespan = np.random.normal(input_spec.age + 100, 10) - input_spec.weight
    simulated_height = np.random.normal(170, 10)

    index_data = input_spec.model_dump(mode="json")
    multi_index = make_onerow_multiindex_from_dict(index_data)
    results_df = pd.DataFrame(
        data={
            "lifespan": [simulated_lifespan],
            "height": [simulated_height],
        },
        index=multi_index,
    )

    experiment_metrics = pd.DataFrame(
        data={
            "simulation_runtime": [100],
            "energy_used": [100],
            "memory_used": [100],
            "cpu_time": [100],
        },
        index=multi_index,
    )

    return ExperimentOutputSpec(
        dataframes={
            "simulated_lifespan": results_df,
            "metrics": experiment_metrics,
        },
    )
