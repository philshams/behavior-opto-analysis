from opto_analysis.settings_objects import Tracking_settings

# select the analysis settings
tracking_settings = Tracking_settings(

    redo_dlc_tracking=False,
    redo_processing_step=True,

    min_confidence_in_tracking=0.99,
    max_deviation_from_rest_of_points=60, # in pixels
    display_tracking_output=True, # show a plot of tracking data

    by_experiment=False,
    experiments = [''],

    by_session=True,
    sessions=[0],

    by_prev_session=False,
    prev_session=[0],

    dlc_settings_file='.\\sample_data\\dlc_config.yaml',
    inverse_fisheye_correction_file = '.\\sample_data\\inverse_fisheye_maps.npy' # remove setting if n/a
)
