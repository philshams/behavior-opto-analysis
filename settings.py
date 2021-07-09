from opto_analysis.settings_objects import Processing_settings, Analysis_settings

# select the analysis settings
processing_settings = Processing_settings(

    create_new_metadata=False,
    examine_laser_trials=True,
    examine_audio_trials=False,
    rapid=True, # speed up laser and audio trial clips

    dlc_tracking=False,

    by_experiment=False,
    experiments = ['block edge vectors'],

    by_session=True,
    sessions=[0,1],

    by_prev_session=False,
    prev_session=[0]

)

# select the plotting settings
analysis_settings_name = "threat video all"
 


# TODO: make processing settings dynamic, and have plotting programs saved (with specific analysis performed if requested)


#------------list of analysis programs---------------

all_analysis_settings = {}

all_analysis_settings["threat video all"] = Analysis_settings(plot_type='threat video', experiments = 'all')
all_analysis_settings["laser video block edge vectors"] = Analysis_settings(plot_type='laser video', experiments=['block edge vectors'])

analysis_settings=all_analysis_settings[analysis_settings_name]