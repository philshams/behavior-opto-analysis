# select the analysis program you would like to run
settings_name = "verify the first session"
 
# TODO: make processing settings dynamic, and have plotting programs saved (with specific analysis performed if requested)


#------------list of analysis programs---------------
from opto_analysis.settings import Analysis_settings
programs = {}

programs["process all experiments"] = Analysis_settings()
programs["verify the first session"] = Analysis_settings(verify_data_sync=True, load_metadata=False, by_session=True, sessions=[0,1])
programs["process block edge vectors"] = Analysis_settings(verify_data_sync=True, by_experiment=True, experiments=['block edge vectors'])

settings=programs[settings_name]