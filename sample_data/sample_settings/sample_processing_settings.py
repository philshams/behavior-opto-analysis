from opto_analysis.settings_objects import Processing_settings

# select the analysis settings
processing_settings = Processing_settings(

    create_new_registration = False, #! If you redo the registration, please update the checksums in test_track
    skip_registration = False,
    fisheye_correction_file = ".\\sample_data\\fisheye_maps.npy", # remove setting if n/a
    size = 1024, # how big to make the renderings, in square pixels; currently must be >920
    pixels_per_cm = 10, # for the arena drawn in register.generate_rendered_arena, report here the ratio between size of arena in pixels and actual size in cm

    by_experiment=True,
    experiments = ['block edge vectors'],

    by_session=True,
    sessions=[0, 1, 2],

    by_prev_session=False,
    prev_session=[0],

)
