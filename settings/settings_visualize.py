from opto_analysis.utils.settings_objects import Settings_visualize

settings_visualize = Settings_visualize(

    laser_trials=False,
    escape_trials=False,
    homing_trials = True,
    
    display_trail=True,
    display_tracking=False,

    display_stimulus = True,
    rapid = True,

    seconds_before_audio = 3,
    seconds_before_laser = 3,
    seconds_before_homing = 3,
    seconds_after_audio = 2,
    seconds_after_laser = 6,
    seconds_after_homing = 3,

    save_folder = "D:\\data\\Paper II\\trial clips\\",

    by_experiment=False,
    experiments = [''],

    by_session=True,
    sessions=[28],
)
