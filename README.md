[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
[![codecov](https://codecov.io/gh/philshams/opto-analysis/branch/master/graph/badge.svg?token=IDLENSLEP4)](https://codecov.io/gh/philshams/opto-analysis)

# opto analysis

Opto analysis is a package for analyzing free-moving behavioral data during optogenetics experiments. It is currently optimized for and tested on Windows terminals with debugging in VS Code, but it can be extended to other systems upon request. 

## Installation

- Clone the repository
- Get the sample data at "...Dropbox (UCL)\DAQ\upstairs_rig\21MAR16_9718_block evs"; place this folder in the sample_data folder
- **Users**: Can make a new Python 3.8 environment and install the requirements:
```pip install -r requirements.txt```
- **Devs**: Create a new python environment using the environment file: ```conda env create -f environment.yml``` or create a new Python 3.8 environment and install the dev requirements: ```pip install -r dev_requirements.txt```
- Navigate to the opto-analysis folder and write the command ```pip install -e .```

## Usage

- To process data and verify synchronization, fill in the the file ./settings/processing_settings.py with your desired settings, and run the terminal command ```process```
- To track data (DeepLabCut), fill in the the file ./settings/tracking_settings.py with your desired settings, and run the command ```track```
- To visualize trials, fill in the the file ./settings/visualization_settings.py with your desired settings, and run the command ```visualize```. This currently requires having already trained a DLC network.
- To analyze and plot data, fill in the the file ./settings/analysis_settings.py with your desired settings, and run the command ```analyze```

## Testing (devs)
- In VS code: run test discovery and then run or debug the desired tests in the Test Explorer. Run each test in "./tests/test_run.py" to debug an entire workflow (processing, tracking, visualization, analysis)
- In the terminal:
```python
pytest # run all tests
pytest tests/test_file.py # test one file (you must be in from the parent directory of 'tests' to run this)
```
- To examine the test coverage, run in the terminal: ```pytest --cov-report term-missing --cov=opto_analysis tests/```
<br/><br/>
- To instead generate a coverage report, run: ```pytest --cov-report xml --cov=opto_analysis tests/```
<br/>...and then run in bash shell: ```bash <(curl -s https://codecov.io/bash) -t TOKEN-NUMBER```

