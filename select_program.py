# select the analysis program you would like to run
program_name = "process all experiments"
 

#------------list of analysis programs---------------
from opto_analysis.options import Options
programs = {}

programs["process all experiments"] = Options(process_data=True)
programs["process the first session"] = Options(process_data=True, analyze_particular_sessions=True, sessions_to_analyze=[0])

program=programs[program_name]