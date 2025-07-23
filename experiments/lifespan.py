import numpy as np

from scythe.base import ExperimentInputSpec, ExperimentOutputSpec, FileReference
from scythe.registry import ExperimentRegistry


class LifespanExperimentInputs(ExperimentInputSpec):
    age: int
    weight: float
    coeffs: FileReference


class LifespanExperimentOutputs(ExperimentOutputSpec):
    lifespan: float
    height: float
    simulation_runtime: float
    energy_used: float
    memory_used: float
    cpu_time: float


@ExperimentRegistry.Register()
def simulate_lifespan(
    input_spec: LifespanExperimentInputs,
) -> LifespanExperimentOutputs:
    simulated_lifespan = np.random.normal(input_spec.age + 100, 10) - input_spec.weight
    simulated_height = np.random.normal(170, 10)

    return LifespanExperimentOutputs(
        lifespan=simulated_lifespan,
        height=simulated_height,
        simulation_runtime=100,
        energy_used=100,
        memory_used=100,
        cpu_time=100,
    )
