from opto_analysis.settings_objects import Visualization_settings

# select the analysis settings
visualization_settings = Visualization_settings(

    laser_video=True,
    escape_video=True,
    generate_rendering=False,
    visualize_exploration=False,

    by_experiment=False,
    experiments = [''],

    by_session=True,
    sessions=[0, 1],

    by_prev_session=False,
    prev_session=[0]
)
