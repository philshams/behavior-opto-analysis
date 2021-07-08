from opto_analysis.program import Program
from data_bank import all_sessions
import numpy as np

def select_sessions_to_analyze(program: Program) -> object:
    selected_sessions = np.array(all_sessions, dtype='object')

    if program.analyze_particular_experiments:
        assert isinstance(program.experiments_to_analyze, list), "Experiment(s) must be listed in list format"
        experiments_idx = np.sum([experiment==selected_sessions[:,2] for experiment in program.experiments_to_analyze],0).astype(bool)
        selected_sessions = selected_sessions[experiments_idx]

    if program.analyze_particular_naivete:
        assert isinstance(program.num_previous_sessions_to_analyze, list), "Number(s) of previous sessions must be listed in list format"
        naivete_idx = np.sum([num_prev_sessions==selected_sessions[:,3] for num_prev_sessions in program.num_previous_sessions_to_analyze],0).astype(bool)
        selected_sessions = selected_sessions[naivete_idx]

    if program.analyze_particular_sessions:
        assert isinstance(program.sessions_to_analyze, list), "Session number(s) must be listed in list format"
        session_idx = np.sum([session_num==selected_sessions[:,0] for session_num in program.sessions_to_analyze],0).astype(bool)
        selected_sessions = selected_sessions[session_idx]

    return selected_sessions
    


