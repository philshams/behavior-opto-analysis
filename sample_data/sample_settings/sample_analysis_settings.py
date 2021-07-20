from opto_analysis.settings_objects import Analysis_settings

analysis_settings_selection = "threat video all"
 




selection = {}
#------------selection of analysis settings to choose from--------------

selection["threat video all"] = \
    Analysis_settings(plot_type='threat video')
    
selection["laser video block edge vectors"] = \
    Analysis_settings(plot_type='laser video', experiments=['block edge vectors'])

#-----------------------------------------------------------------------
analysis_settings=selection[analysis_settings_selection]