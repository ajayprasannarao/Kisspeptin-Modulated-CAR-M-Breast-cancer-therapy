# Breast Therapy Pipeline Simulation

A Python simulation of a target-enriched breast-carcinoma clinical-trial cohort. The project generates a heterogeneous patient cohort and evaluates a logical treatment gate using tissue stiffness and cellular identity markers.

## Features

- Generates synthetic breast-carcinoma patient cohorts.
- Models HER2 and TP53-related cellular characteristics.
- Applies a stiffness safety window from `0.0` through `5.0`.
- Combines stiffness and biomarker checks to determine whether the treatment gate fires.
- Runs a configurable breast-therapy pipeline with a reproducible random seed.

## Requirements

- Python 3.9 or newer
- NumPy

Install the dependency with:

```bash
python -m pip install numpy
```

## Usage

Run the simulation from the project directory:

```bash
python main2.py
```

The main pipeline can also be imported and configured from Python:

```python
from main2 import execute_breast_therapy_pipeline

results = execute_breast_therapy_pipeline(
    kisspeptin_dose=10.0,
    num_patients=1000,
    seed=42,
)
```

The random seed makes repeated runs reproducible. Adjust `num_patients`, `kisspeptin_dose`, and `seed` to explore other simulation scenarios.

## Breast profile

The default breast-carcinoma profile is configured as:

```python
SolidTumorProfile("Breast Carcinoma", 0.2, 20.0, "HER2", 0.85, 0.40)
```

The stiffness input is accepted when it falls within the inclusive range `0.0 <= stiffness <= 5.0`. Patients outside this range fail the stiffness input check.

## Project structure

```text
.
├── main2.py   # Cohort generation and therapy-pipeline simulation
└── README.md  # Project documentation
```

## Notes

This repository contains a computational simulation and is not a clinical decision-support system. Its synthetic outputs should not be used to guide patient care or treatment decisions.

## License

No license has been specified yet. Add a license before distributing the project publicly.
