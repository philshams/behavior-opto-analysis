from opto_analysis.utils.settings_objects import Settings_analyze_global as Settings_analyze
from settings.analyses import analyses

settings_analyze = Settings_analyze(

analysis = analyses["escape targets compare"], 
# see types_of_analysis.py for options

max_num_trials = 6,
max_escape_duration = 9,
post_laser_seconds_to_plot = 5,
min_distance_from_shelter = 10,
escape_initiation_speed = 30,
edge_vector_threshold = 0.65,
two_tailed_test = True,

x_jitter = True,
color_by = 'target', 
# 'session' 'trial' ''  (for all)
# 'speed' 'time'        (for trajectories)
# 'target'              (for escape targets)

save_folder = "D:\\data\\Paper II"

)

