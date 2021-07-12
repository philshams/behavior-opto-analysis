from opto_analysis.settings_objects import Tracking_settings

# select the analysis settings
tracking_settings = Tracking_settings(

    dlc_settings_file='D:\\data\\DLC_nets\\Barnes-Philip-2020-12-07\\config.yaml',

    by_experiment=False,
    experiments = [''],

    by_session=True,
    sessions=[0, 1],

    by_prev_session=False,
    prev_session=[0]
)
