from opto_analysis.settings_objects import Visualization_settings

# select the analysis settings
visualization_settings = Visualization_settings(

    visualize_laser_trials=False,
    visualize_escape_trials=True,
    generate_rendering=False,
    rapid = True,
    verbose = True,
    size = 1024, # how big to make the visualizations, in square pixels

    visualize_exploration=False,

    save_folder = "D:\\data\\Paper II",

    fisheye_correction_file = ".\\sample_data\\fisheye_maps.npy", # remove setting if n/a

    by_experiment=False,
    experiments = [''],

    by_session=True,
    sessions=[0],

    by_prev_session=False,
    prev_session=[0]
)
