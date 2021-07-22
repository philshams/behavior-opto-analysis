from opto_analysis.settings_objects import Settings_visualize

# select the analysis settings
settings_visualize = Settings_visualize(

    visualize_laser_trials=True,
    visualize_escape_trials=False,
    
    display_tracking=False,
    display_trail=True,

    display_stim_status = True,
    rapid = True,
    
    generate_rendering=False,

    seconds_before_audio = 3,
    seconds_before_laser = 3,
    seconds_after_audio = 2,
    seconds_after_laser = 6,

    save_folder = ".\\sample_data",

    by_experiment=False,
    experiments = [''],

    by_session=True,
    sessions=[0],

    by_prev_session=False,
    prev_session=[0]
)
