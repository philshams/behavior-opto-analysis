from opto_analysis.settings_objects import Visualization_settings

# select the analysis settings
visualization_settings = Visualization_settings(

    visualize_laser_trials=False,
    visualize_escape_trials=True,
    
    display_tracking=False,
    display_trail=True,

    display_stim_status = True,
    rapid = True,
    
    generate_rendering=False,

    seconds_before_audio = 3,
    seconds_before_laser = 3,
    seconds_after_audio = 2,
    seconds_after_laser = 6,

    save_folder = "C:\\data\\Paper II",

    by_experiment=False,
    experiments = [''],

    by_session=True,
    sessions=[0, 1],

    by_prev_session=False,
    prev_session=[0]
)
