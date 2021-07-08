# select the analysis program you would like to run
program_name = "process block edge vectors"
 

#------------list of analysis programs---------------
from opto_analysis.program import Program
programs = {}

programs["process all experiments"] = Program(process_data=True)
programs["process the first session"] = Program(process_data=True, analyze_particular_sessions=True, sessions_to_analyze=[0])
programs["process block edge vectors"] = Program(process_data=True, analyze_particular_experiments=True, experiments_to_analyze=['fake experiment','block edge vectors'])

program=programs[program_name]