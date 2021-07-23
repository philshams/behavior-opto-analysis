from opto_analysis.utils.settings_objects import Settings_visualize

settings_visualize = Settings_visualize(

    laser_trials=False,
    escape_trials=True,
    
    display_trail=False,
    display_tracking=True,

    display_stimulus = True,
    rapid = True,

    seconds_before_audio = 3,
    seconds_before_laser = 3,
    seconds_after_audio = 2,
    seconds_after_laser = 6,

    save_folder = "D:\\data\\Paper II",

    by_experiment=False,
    experiments = [''],

    by_session=True,
    sessions=[0],

    by_prev_session=False,
    prev_session=[0]
)
