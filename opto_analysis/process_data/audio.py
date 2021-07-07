from opto_analysis.process_data.session import Session
import os
import numpy as np
from dataclasses import dataclass
from typing import Tuple
from glob import glob

@dataclass(frozen=True)
class Audio:
    num_samples: int
    onset_frames: object
    stimulus_durations: object
    amplitude: object

def get_Audio(session: Session) -> Audio:
    AI_file = glob(os.path.join(session.file_path, "analog*"))[-1] # take the last file if there are multiple
    AI_data = np.fromfile(AI_file)

    audio_data = AI_data[np.arange(1, len(AI_data), 4)] # four interleaved time series

    audio_num_samples = len(audio_data)
    audio_onset_frames, stimulus_durations, amplitude = get_audio_stimulus_parameters(audio_data, session)
    audio = Audio(audio_num_samples, audio_onset_frames, stimulus_durations, amplitude)
    return audio

def get_audio_stimulus_parameters(audio_data: object, session: Session) -> Tuple[object, object, object]:
    
    audio_on_idx = np.where(abs(audio_data)>1.25)[0]
    idx_since_audio_on = np.append(np.inf, np.diff(audio_on_idx)) # get the first sample of audio stimuli
    audio_onset_idx = audio_on_idx[idx_since_audio_on > (session.daq_sampling_rate * 30)] # separate trials separated by > 30 sec
    audio_onset_frames = np.round(audio_onset_idx / session.daq_sampling_rate * session.fps).astype(int)

    idx_before_next_audio = np.append(np.diff(audio_on_idx[::-1]), -np.inf) # get the last sample of audio stimuli
    audio_offset_idx = audio_on_idx[idx_before_next_audio < -(session.daq_sampling_rate * 30)]
    stimulus_durations = np.round((audio_offset_idx-audio_onset_idx) / session.daq_sampling_rate, 1)

    amplitude = np.round(np.array([np.sqrt(np.sum(audio_data[audio_onset_idx[i]:audio_offset_idx[i]]**2)) for i in range(len(audio_onset_idx))]) * .2625) # scaling to make it ~dB

    return audio_onset_frames, stimulus_durations, amplitude