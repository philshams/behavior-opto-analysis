import numpy as np
from typing import Tuple

def get_onset_and_duration(data_on: object, session: object, stim_type: str, min_frames_between_trials: int, round_durations: bool) -> Tuple[object, object, object]:
    
    data_on_idx = np.where(data_on)[0]

    if not data_on_idx.size:
        print("No {} trials detected".format(stim_type))
        return [],[]

    idx_since_data_on     = np.append(np.inf, np.diff(data_on_idx)) 
    data_onset_idx        = data_on_idx[idx_since_data_on > min_frames_between_trials]
    data_onset_frames     = np.array([[np.argmin(abs(x - session.camera_trigger.frame_trigger_onsets_idx))] for x in data_onset_idx])
    idx_before_next_trial = np.append(-np.inf, np.diff(data_on_idx[::-1]))[::-1]
    data_offset_idx       = data_on_idx[idx_before_next_trial < -min_frames_between_trials]
    data_offset_frames    = np.array([[np.argmin(abs(x - session.camera_trigger.frame_trigger_onsets_idx))] for x in data_offset_idx])

    if round_durations:
        stimulus_durations = np.array([[x] for x in np.round((data_offset_idx-data_onset_idx) / session.daq_sampling_rate, 1)])
    if not round_durations: 
        stimulus_durations = np.array([[x] for x in (data_offset_idx-data_onset_idx) / session.daq_sampling_rate])

    return data_onset_frames, stimulus_durations, data_offset_frames