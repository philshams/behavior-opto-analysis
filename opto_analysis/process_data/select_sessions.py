from opto_analysis.settings import Analysis_settings
from data_bank import all_data_entries
import numpy as np

def select_sessions_to_analyze(program: Analysis_settings) -> object:
    selected_sessions = np.array(all_data_entries, dtype='object')

    if program.by_experiment:
        assert isinstance(program.experiments, list), "Experiment(s) must be listed in list format"
        experiments_idx = np.sum([experiment==selected_sessions[:,2] for experiment in program.experiments],0).astype(bool)
        selected_sessions = selected_sessions[experiments_idx]

    if program.by_prev_session:
        assert isinstance(program.prev_session, list), "Number(s) of previous sessions must be listed in list format"
        naivete_idx = np.sum([num_prev_sessions==selected_sessions[:,3] for num_prev_sessions in program.prev_session],0).astype(bool)
        selected_sessions = selected_sessions[naivete_idx]

    if program.by_session:
        assert isinstance(program.sessions, list), "Session number(s) must be listed in list format"
        session_idx = np.sum([session_num==selected_sessions[:,0] for session_num in program.sessions],0).astype(bool)
        selected_sessions = selected_sessions[session_idx]

    return selected_sessions
    


