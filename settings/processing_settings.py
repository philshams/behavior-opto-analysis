from opto_analysis.settings_objects import Processing_settings

# select the analysis settings
processing_settings = Processing_settings(

    create_new_metadata=True,

    examine_laser_trials=False,
    examine_audio_trials=False,
    rapid=False, # speed up laser and audio trial clips

    by_experiment=False,
    experiments = [''],

    by_session=True,
    sessions=[0, 1],

    by_prev_session=False,
    prev_session=[0],

)
