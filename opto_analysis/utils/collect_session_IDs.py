import numpy as np
import os
from typing import Tuple

def collect_session_IDs(settings: object, databank: dict, group_num: int=0) -> np.ndarray:
    session_IDs = np.array(databank['session IDs'], dtype='object')
    if settings.by_experiment:
        if group_num: key = 'group_' + str(group_num)
        else:         key = 'experiments'
        factor_idx = 2
    if settings.by_prev_session:
        if group_num: key = 'group_' + str(group_num)
        else:         key = 'prev_session'
        factor_idx = 3
    if settings.by_session:
        if group_num: key = 'group_' + str(group_num)
        else:         key = 'sessions'
        factor_idx = 0
    if settings.by_experiment or settings.by_prev_session or settings.by_session:
        assert isinstance(settings.__dict__[key], list), "Group must be listed in list format" 
        group_idx = np.sum([factor==session_IDs[:,factor_idx] for factor in settings.__dict__[key]],0).astype(bool)
        session_IDs = session_IDs[group_idx]   
    
    for entry in session_IDs: # add in the full path to the raw data
        entry[4] = os.path.join(databank['path'], entry[4])
    
    # add the group name to the list of details
    session_IDs = np.array([np.append(session_ID, group_num) for session_ID in session_IDs])

    return session_IDs

def collect_session_IDs_analysis(settings: object, databank: dict) -> np.ndarray:
    if not settings.compare:
        session_IDs = collect_session_IDs(settings, databank)
    if settings.compare:
        assert int(settings.by_experiment + settings.by_prev_session + settings.by_session)==1,"Must select exactly one factor to compare between"
        session_IDs = np.empty((0,6))
        for group_num in range(1,8):
            session_IDs_group_i = collect_session_IDs(settings, databank, group_num) 
            session_IDs = np.concatenate((session_IDs, session_IDs_group_i))

    return session_IDs