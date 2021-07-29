from opto_analysis.process.session import Session
import os
import numpy as np
from dataclasses import dataclass
from typing import Tuple
from glob import glob
import dill as pickle

@dataclass(frozen=True)
class Audio:
    num_samples: int
    onset_frames: object
    stimulus_durations: object

def get_Audio(session: Session) -> Audio:
    AI_file = glob(os.path.join(session.file_path, "analog*"))[-1] # take the last file if there are multiple
    try:
        with open(AI_file, "rb") as dill_file: AI_data = pickle.load(dill_file)
    except:
        AI_data = np.fromfile(AI_file)
    audio_data = AI_data[np.arange(1, len(AI_data), 4)] # four interleaved time series
    audio_num_samples = len(audio_data)
    audio_onset_frames, stimulus_durations = get_audio_stimulus_parameters(audio_data, session)
    audio = Audio(audio_num_samples, audio_onset_frames, stimulus_durations)
    return audio

def get_audio_stimulus_parameters(audio_data: object, session: Session) -> Tuple[object, object, object]:
    
    audio_on_idx = np.where(abs(audio_data)>3)[0]
    idx_since_audio_on = np.append(np.inf, np.diff(audio_on_idx)) # get the first sample of audio stimuli
    audio_onset_idx = audio_on_idx[idx_since_audio_on > (session.daq_sampling_rate * 30)] # separate trials separated by > 30 sec
    audio_onset_frames = np.array([[np.argmin(abs(x - session.camera_trigger.frame_trigger_onsets_idx))] for x in audio_onset_idx])
    
    idx_before_next_audio = np.append(-np.inf, np.diff(audio_on_idx[::-1]))[::-1] # get the last sample of audio stimuli
    audio_offset_idx = audio_on_idx[idx_before_next_audio < -(session.daq_sampling_rate * 30)]
    stimulus_durations =np.array([[x] for x in np.round((audio_offset_idx-audio_onset_idx) / session.daq_sampling_rate, 1)])

    return audio_onset_frames, stimulus_durations