from opto_analysis.utils.settings_objects import Settings_track

settings_track = Settings_track(

    redo_processing_step=False,

    min_confidence_in_tracking=0.5,
    max_deviation_from_rest_of_points=100, # in pixels
    display_tracking_output=False, # show a plot of tracking data

    by_experiment=False,
    experiments = ['open field'],

    by_session=True,
    sessions=[x for x in [27]],

    dlc_settings_file='D:\\data\\DLC_nets\\opto-philip-2021-07-26\\config.yaml',
    inverse_fisheye_correction_file = '.\\sample_data\\inverse_fisheye_maps.npy' # remove setting if n/a
)
