from opto_analysis.settings_objects import Processing_settings

# select the analysis settings
processing_settings = Processing_settings(

    create_new_metadata=True,

    examine_laser_trials=False,
    examine_audio_trials=True,
    rapid=True, # speed up laser and audio trial clips

    dlc_tracking=False,

    by_experiment=False,
    experiments = ['block edge vectors'],

    by_session=True,
    sessions=[0, 1],

    by_prev_session=False,
    prev_session=[0],

)
