from opto_analysis.utils.settings_objects import Settings_analyze

settings_analyze_selection = "threat video all"
 




selection = {}
#------------selection of analysis settings to choose from--------------

selection["threat video all"] = \
    Settings_analyze(plot_type='threat video')
    
selection["laser video block edge vectors"] = \
    Settings_analyze(plot_type='laser video', experiments=['block edge vectors'])

#-----------------------------------------------------------------------
settings_analyze=selection[settings_analyze_selection]