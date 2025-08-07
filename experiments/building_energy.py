from typing import Literal

from pydantic import Field
from scythe.base import ExperimentInputSpec, ExperimentOutputSpec
from scythe.registry import ExperimentRegistry
from scythe.type_helpers import FileReference


class BuildingSimulationInput(ExperimentInputSpec):
    """Simulation inputs for a building energy model."""

    r_value: float = Field(
        default=..., description="The R-Value of the building [m2K/W]", ge=0, le=15
    )
    lpd: float = Field(
        default=..., description="Lighting power density [W/m2]", ge=0, le=20
    )
    setpoint: float = Field(
        default=..., description="Thermostat setpoint [deg.C]", ge=12, le=30
    )
    economizer: Literal[
        "NoEconomizer", "DifferentialDryBulb", "DifferentialEnthalpy"
    ] = Field(
        default=...,
        description="The type of economizer to use",
    )
    weather_file: FileReference = Field(default=..., description="Weather file [.epw]")
    design_day_file: FileReference = Field(
        default=..., description="Weather file [.ddy]"
    )


class BuildingSimulationOutput(ExperimentOutputSpec):
    """Simulation outputs for a building energy model."""

    heating: float = Field(
        default=..., description="Annual heating energy usage, kWh/m2", ge=0
    )
    cooling: float = Field(
        default=..., description="Annual cooling energy usage, kWh/m2", ge=0
    )
    lighting: float = Field(
        default=..., description="Annual lighting energy usage, kWh/m2", ge=0
    )
    equipment: float = Field(
        default=..., description="Annual equipment energy usage, kWh/m2", ge=0
    )
    fans: float = Field(
        default=..., description="Annual fans energy usage, kWh/m2", ge=0
    )
    pumps: float = Field(
        default=..., description="Annual pumps energy usage, kWh/m2", ge=0
    )


@ExperimentRegistry.Register()
def simulate_energy(input_spec: BuildingSimulationInput) -> BuildingSimulationOutput:
    """Initialize and execute an energy model of a building."""

    # do some work!

    return BuildingSimulationOutput(
        heating=0,
        cooling=0,
        lighting=0,
        equipment=0,
        fans=0,
        pumps=0,
        dataframes={},
    )
