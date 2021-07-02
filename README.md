[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
[![Python package](https://github.com/philshams/opto-analysis/actions/workflows/github-actions.yml/badge.svg)](https://github.com/philshams/opto-analysis/actions/workflows/github-actions.yml)
[![codecov](https://codecov.io/gh/philshams/opto-analysis/branch/master/graph/badge.svg?token=IDLENSLEP4)](https://codecov.io/gh/philshams/opto-analysis)

# opto analysis

Opto analysis is a package used in the Branco lab for analyzing free-moving behavioral data during optogenetics experiments.

## Installation

- Clone the repository
- Users: Can make a new Python 3.8 environment and install the requirements:
```pip install -r requirements.txt```
- Devs: Create a new python environment using the environment file: ```conda env create -f environment.yml``` or create a new Python 3.8 environment and install the dev requirements: ```pip install -r requirements.txt```
- Navigate to the opto-analysis folder and write the command ```pip install -e .```

## Usage

- You can run or debug the code in an IDE or from the terminal, as follows
```python
python -m opto_analysis.run # does X
```

## Testing
- Run test discovery in VS code, and run or debug them using the Test Explorer
- Alternatively, run tests in the terminal:
```python
pytest # run all tests (from any part of the repo directory)
pytest -pdb
pytest tests/test_file.py # must be in the parent directory of 'tests'; this will just test "file"
```

