from opto_analysis.utils.settings_objects import Settings_analyze_global as Settings_analyze
from settings.analyses import analyses

settings_analyze = Settings_analyze(

analysis = analyses["laser"], 
# see types_of_analysis.py for options

max_escapes_per_mouse = 6,
max_seconds_to_reach_shelter = 9,

color_by = '', 
# 'speed' 'session' 'time' 'trial' or ''

save_folder = "D:\\data\\Paper II"


)

