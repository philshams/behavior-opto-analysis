[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
[![codecov](https://codecov.io/gh/philshams/opto-analysis/branch/master/graph/badge.svg?token=IDLENSLEP4)](https://codecov.io/gh/philshams/opto-analysis)

# opto analysis

Opto analysis is a package for analyzing free-moving behavioral data during optogenetics experiments. It is currently optimized for and tested on Windows terminals with debugging in VS Code, but it can be extended to other systems upon request. 

## Installation

- Clone the repository

- Get the sample data at "...Dropbox (UCL)\DAQ\upstairs_rig\21MAR16_9718_block evs"; place this folder in the sample_data folder

- Navigate to the opto-analysis folder and run the following commands:

  - **Users**: Create a new Python 3.8 environment (default name "opto-user") with ```conda env create -f environment_user.yml```

  - **Devs**: Create a new Python 3.8 environment (default name "opto") with ```conda env create -f environment_dev.yml```

  - **Both**: Install the package with the command ```pip install -e .```

## Usage

- To process data and verify synchronization, fill in the the file *./settings/settings_process.py* with your desired settings, and run the terminal command ```process```

- To track data (DeepLabCut), fill in the the file *./settings/settings_track.py* with your desired settings, and run the command ```track```

- To visualize trials, fill in the the file *./settings/settings_visualize.py* with your desired settings, and run the command ```visualize```. This  requires a trained DLC network.

- To analyze and plot data, fill in the the file *./settings/analyses* with your desired analysis program options and then fill in *./settings/settings_analyze.py* with your desired global analysis settings (including the program you'd like to run), and run the command ```analyze```

## Testing (devs)
- In VS code: run test discovery and then run or debug the desired tests in the Test Explorer. Run each test in *./tests/test_run.py* to debug an entire workflow (processing, tracking, visualization, analysis)

- Alternatively, run in the terminal: ```pytest``` or ```pytest tests/test_file.py```

- To examine the test coverage, run: ```pytest --cov-report term-missing --cov=opto_analysis tests/```


- To instead generate a coverage report, run: ```pytest --cov-report xml --cov=opto_analysis tests/```

- ...and then run in bash shell: ```bash <(curl -s https://codecov.io/bash) -t TOKEN-NUMBER``` to upload to codecov

## Dependency management

- To remake the environment file, run: ```conda env export > dev_environment.yml```




