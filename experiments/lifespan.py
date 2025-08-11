import numpy as np

from pydantic import Field
from scythe.base import ExperimentInputSpec, ExperimentOutputSpec
from scythe.registry import ExperimentRegistry
from scythe.utils.filesys import FileReference


class LifespanExperimentInputs(ExperimentInputSpec):
    age: int = Field(
        default=..., description="The age of the subject [yrs]", ge=0, le=125
    )
    weight: float = Field(
        default=..., description="The weight of the subject [lbs]", ge=0, le=500
    )
    coeffs: FileReference = Field(
        default=..., description="The coefficients of the model"
    )


class LifespanExperimentOutputs(ExperimentOutputSpec):
    lifespan: float = Field(
        default=..., description="The lifespan of the subject [yrs]"
    )
    height: float = Field(default=..., description="The height of the subject [cm]")
    simulation_runtime: float = Field(
        default=..., description="The runtime of the simulation [s]"
    )
    energy_used: float = Field(
        default=..., description="The energy used by the simulation [J]"
    )
    memory_used: float = Field(
        default=..., description="The memory used by the simulation [MB]"
    )
    cpu_time: float = Field(
        default=..., description="The CPU time used by the simulation [s]"
    )


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
