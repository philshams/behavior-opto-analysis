from opto_analysis.settings_objects import Processing_settings
from settings.data_bank import all_data_entries
import numpy as np

def select_sessions(processing_settings: Processing_settings) -> object:
    selected_sessions = np.array(all_data_entries, dtype='object')

    if processing_settings.by_experiment:
        assert isinstance(processing_settings.experiments, list), "Experiment(s) must be listed in list format"
        experiments_idx = np.sum([experiment==selected_sessions[:,2] for experiment in processing_settings.experiments],0).astype(bool)
        selected_sessions = selected_sessions[experiments_idx]

    if processing_settings.by_prev_session:
        assert isinstance(processing_settings.prev_session, list), "Number(s) of previous sessions must be listed in list format"
        naivete_idx = np.sum([num_prev_sessions==selected_sessions[:,3] for num_prev_sessions in processing_settings.prev_session],0).astype(bool)
        selected_sessions = selected_sessions[naivete_idx]

    if processing_settings.by_session:
        assert isinstance(processing_settings.sessions, list), "Session number(s) must be listed in list format"
        session_idx = np.sum([session_num==selected_sessions[:,0] for session_num in processing_settings.sessions],0).astype(bool)
        selected_sessions = selected_sessions[session_idx]

    return selected_sessions
    


