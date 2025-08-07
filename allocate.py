import json
from pathlib import Path

import boto3
import numpy as np
import pandas as pd
from scythe.allocate import BaseExperiment
from scythe.scatter_gather import RecursionMap

from experiments.building_energy import BuildingSimulationInput, simulate_energy


def sample(n: int = 10) -> pd.DataFrame:
    r_value = np.random.uniform(0, 15, size=n)
    lpd = np.random.uniform(0, 20, size=n)
    setpoint = np.random.uniform(12, 30, size=n)
    economizer = np.random.choice(
        ["NoEconomizer", "DifferentialDryBulb", "DifferentialEnthalpy"], size=n
    )
    weather_file = [
        Path(name)
        for name in np.random.choice(
            [f"{name}" for name in Path("artifacts").glob("*.epw")], size=n
        )
    ]
    design_day_file = [f"artifacts/{Path(name).stem}.ddy" for name in weather_file]
    df = pd.DataFrame(
        {
            "r_value": r_value,
            "lpd": lpd,
            "setpoint": setpoint,
            "economizer": economizer,
            "weather_file": weather_file,
            "design_day_file": design_day_file,
        }
    )
    return df


def allocate(df: pd.DataFrame):

    df["experiment_id"] = "placeholder"
    df["sort_index"] = pd.RangeIndex(len(df))
    specs = [
        BuildingSimulationInput.model_validate(row.to_dict())
        for _, row in df.iterrows()
    ]
    s3_client = boto3.client("s3")

    experiment = BaseExperiment(
        experiment=simulate_energy,
    )

    return experiment.allocate(
        specs,
        version="bumpmajor",
        s3_client=s3_client,
        recursion_map=RecursionMap(factor=2, max_depth=2),
    )


def main():
    specs = sample(10)
    run, ref = allocate(specs)
    print(json.dumps(run.model_dump(mode="json"), indent=2))
    print(ref.workflow_run_id)
    result = ref.result()
    print(result)


if __name__ == "__main__":
    # main()
    exp = BaseExperiment.model_validate(
        BaseExperiment(
            experiment=simulate_energy,
        ).model_dump(mode="json")
    )
    print(exp)
