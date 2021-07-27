import numpy as np
import os
from typing import Tuple

def collect_session_IDs(settings: object, databank: dict, group: str='') -> np.ndarray:
    session_IDs = np.array(databank['session IDs'], dtype='object')

    if settings.by_experiment:
        assert isinstance(settings.__dict__['experiments'+group], list), "Experiment(s) must be listed in list format"
        experiments_idx = np.sum([experiment==session_IDs[:,2] for experiment in settings.__dict__['experiments'+group]],0).astype(bool)
        session_IDs = session_IDs[experiments_idx]

    if settings.by_prev_session:
        assert isinstance(settings.__dict__['prev_session'+group], list), "Number(s) of previous sessions must be listed in list format"
        naivete_idx = np.sum([num_prev_sessions==session_IDs[:,3] for num_prev_sessions in settings.__dict__['prev_session'+group]],0).astype(bool)
        session_IDs = session_IDs[naivete_idx]

    if settings.by_session:
        assert isinstance(settings.__dict__['sessions'+group], list), "Session number(s) must be listed in list format"
        session_idx = np.sum([session_num==session_IDs[:,0] for session_num in settings.__dict__['sessions'+group]],0).astype(bool)
        session_IDs = session_IDs[session_idx]

    for entry in session_IDs: # add in the full path to the raw data
        entry[4] = os.path.join(databank['path'], entry[4])

    return session_IDs

def collect_session_IDs_analysis(settings: object, databank: dict) -> np.ndarray:
    if not settings.compare:
        session_IDs = collect_session_IDs(settings, databank)
    if settings.compare:
        # TODO: group numbers instead of letters, for comparing several groups
        session_IDs_group_A = collect_session_IDs(settings, databank, group='_group_A') 
        session_IDs_group_B = collect_session_IDs(settings, databank, group='_group_B')
        session_IDs_group_A = np.array([np.append(session_ID, 'A') for session_ID in session_IDs_group_A])
        session_IDs_group_B = np.array([np.append(session_ID, 'B') for session_ID in session_IDs_group_B])
        session_IDs = np.concatenate((session_IDs_group_A, session_IDs_group_B))

    return session_IDs