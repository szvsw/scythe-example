from datetime import datetime
from pathlib import Path

import boto3
import dotenv
import numpy as np
import pandas as pd
from scythe.allocate import allocate_experiment
from scythe.scatter_gather import RecursionMap

from experiments.lifespan import LifespanExperimentInputs, simulate_lifespan


def sample(n: int = 10) -> pd.DataFrame:
    age = np.random.normal(50, 10, size=n).astype(int)
    weight = np.random.normal(100, 10, size=n).astype(int)
    df = pd.DataFrame(
        {
            "age": age,
            "weight": weight,
            "coeffs": [
                Path("artifacts/even.json")
                if i % 2 == 0
                else Path("artifacts/odd.json")
                for i in range(len(age))
            ],
        }
    )
    return df


def allocate(df: pd.DataFrame):
    datetimestr = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    experiment_id = f"lifespans/v1/{datetimestr}"
    df["experiment_id"] = experiment_id
    df["sort_index"] = pd.RangeIndex(len(df))
    specs = [
        LifespanExperimentInputs.model_validate(row.to_dict())
        for _, row in df.iterrows()
    ]
    s3_client = boto3.client("s3")
    return allocate_experiment(
        experiment_id=experiment_id,
        experiment=simulate_lifespan,
        specs=specs,
        recursion_map=RecursionMap(
            factor=2,
            max_depth=2,
        ),
        s3_client=s3_client,
    )


def main():
    dotenv.load_dotenv()
    specs = sample()
    ref = allocate(specs)
    print(ref.workflow_run_id)
    result = ref.result()
    print(result)


if __name__ == "__main__":
    main()
