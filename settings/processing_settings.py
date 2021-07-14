from opto_analysis.settings_objects import Processing_settings

# select the analysis settings
processing_settings = Processing_settings(

    create_new_registration = True,
    skip_registration = False,
    fisheye_correction_file = ".\\sample_data\\fisheye_maps.npy", # remove setting if n/a
    size = 1024, # how big to make the renderings, in square pixels; currently must be >920

    by_experiment=False,
    experiments = [''],

    by_session=True,
    sessions=[1],

    by_prev_session=False,
    prev_session=[0],

)
