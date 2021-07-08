[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
[![codecov](https://codecov.io/gh/philshams/opto-analysis/branch/master/graph/badge.svg?token=IDLENSLEP4)](https://codecov.io/gh/philshams/opto-analysis)

# opto analysis

Opto analysis is a package used in the Branco lab for analyzing free-moving behavioral data during optogenetics experiments.

## Installation

- Clone the repository
- Get the sample data at _upcoming..._ and place this folder in the sample_data folder
- Users: Can make a new Python 3.8 environment and install the requirements:
```pip install -r requirements.txt```
- Devs: Create a new python environment using the environment file: ```conda env create -f environment.yml``` or create a new Python 3.8 environment and install the dev requirements: ```pip install -r requirements.txt```
- Navigate to the opto-analysis folder and write the command ```pip install -e .```

## Usage

- You can run or debug run.py code in an IDE or run it from the terminal with ```python -m opto_analysis.run``` or simply ```opto```

## Testing
- Run test discovery in VS code, and run or debug them using the Test Explorer
- Alternatively, run tests in the terminal:
```python
pytest # run all tests (from any part of the repo directory)
pytest tests/test_file.py # must be in the parent directory of 'tests'; this will just test "file"
```
- To examine the test coverage, run in the terminal: ```pytest --cov-report term-missing --cov=opto_analysis tests/```
<br/><br/>
- To instead generate a coverage report, run instead: ```pytest --cov-report xml --cov=opto_analysis tests/```
- ...and then run in bash shell: ```bash <(curl -s https://codecov.io/bash) -t TOKEN-NUMBER```

