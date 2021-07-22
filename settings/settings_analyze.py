from opto_analysis.utils.settings_objects import Settings_analyze

settings_visualize = Settings_analyze(

settings_name = "escapes 1",
save_folder = "D:\\data\\Paper II",
max_escapes_per_mouse = 6

)

settings_dict = {}
#------------selection of analysis settings to choose from--------------

settings_dict["escapes 1"] = \
    Settings_analyze(plot_escapes = True, experiments=['block edge vectors'])
    
settings_dict["laser 1"] = \
    Settings_analyze(plot_laser_responses=True, experiments=['block edge vectors'], save_folder=save_folder)

#-----------------------------------------------------------------------
settings_analyze=settings_dict[settings_name]