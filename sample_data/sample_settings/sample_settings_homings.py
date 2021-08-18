from opto_analysis.utils.settings_objects import Settings_homings

# select the homings settings
settings_homings = Settings_homings(

    fast_speed                    = 10,
    padding_duration              = 1,
    heading_dir_threshold_angle   = 30,
    fast_angular_speed            = 90,
    min_change_in_dist_to_shelter = .3,
    threat_area_width             = 600,
    threat_area_height            = 282, # distance from top of frame
    subgoal_locations             = [(512-250, 512),(512+250, 512)],

    by_experiment=False,
    experiments = [''],

    by_session=True,
    sessions=[0, 1]

)
