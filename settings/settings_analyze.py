from opto_analysis.utils.settings_objects import Settings_analyze_global as Settings_analyze
from settings.analyses import analyses

settings_analyze = Settings_analyze(

analysis = analyses["homings test"], 
# see types_of_analysis.py for options

max_num_trials = 6,
max_escape_duration = 9,
post_laser_seconds_to_plot = 0,
min_distance_from_shelter = 10,
escape_initiation_speed = 20,
edge_vector_threshold = 0.68,
two_tailed_test = True,

leftside_only = False,
rightside_only = False,
reflect_trajectories = False,

color_by = 'default', 
# 'default' 'session' 'trial' 'target'  ''  || for all
# 'speed'   'time'    'speed+RT'            || for trajectories

save_folder = "D:\\data\\Paper II\\statistics"

)

