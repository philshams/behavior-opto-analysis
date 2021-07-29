from opto_analysis.utils.settings_objects import Settings_process

settings_process = Settings_process(

    create_new_registration = False,
    skip_registration = True,
    fisheye_correction_file = ".\\sample_data\\fisheye_maps.npy", # remove setting if n/a
    size = 1024, # how big to make the renderings, in square pixels; currently must be >920
    pixels_per_cm = 10, # for the arena drawn in register.generate_rendered_arena, report here the ratio between size of arena in pixels and actual size in cm

    by_experiment=False,
    experiments = [''],

    by_session=True,
    sessions=[x for x in range(71,80)],

    by_prev_session=False,
    prev_session=[0],

)
