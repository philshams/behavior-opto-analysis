[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
[![codecov](https://codecov.io/gh/philshams/opto-analysis/branch/master/graph/badge.svg?token=IDLENSLEP4)](https://codecov.io/gh/philshams/opto-analysis)

# opto analysis

Opto analysis is a package used in the Branco lab for analyzing free-moving behavioral data during optogenetics experiments. It is currently optimized for and tested on Windows terminals with debugging using VS Code, but it can be extended to other systems upon request. 

## Installation

- Clone the repository
- Get the sample data at "...Dropbox (UCL)\DAQ\upstairs_rig\21MAR16_9718_block evs"; place this folder in the sample_data folder
- **Users**: Can make a new Python 3.8 environment and install the requirements:
```pip install -r requirements.txt```
- **Devs**: Create a new python environment using the environment file: ```conda env create -f environment.yml``` or create a new Python 3.8 environment and install the dev requirements: ```pip install -r dev_requirements.txt```
- Navigate to the opto-analysis folder and write the command ```pip install -e .```

## Usage

- You can process data with the command ```python -m opto_analysis.run.process data``` or simply ```process```
- You can analyze data with the command ```python -m opto_analysis.run.analyze_data``` or simply ```analyze```  
- To debug the workflow with VS Code, debug the the file "./tests/test_run.py"

## Testing (devs)
- Using VS code: run test discovery and then run or debug the desired tests in the Test Explorer
- Using the terminal:
```python
pytest # run all tests
pytest tests/test_file.py # test one file; must be run from the parent directory of 'tests'
```
- To examine the test coverage, run in the terminal: ```pytest --cov-report term-missing --cov=opto_analysis tests/```
<br/><br/>
- To instead generate a coverage report, run instead: ```pytest --cov-report xml --cov=opto_analysis tests/```
- ...and then run in bash shell: ```bash <(curl -s https://codecov.io/bash) -t TOKEN-NUMBER```

