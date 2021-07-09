from opto_analysis.process_data.session import Session
import os
import numpy as np
from dataclasses import dataclass
from glob import glob

@dataclass(frozen=True)
class Camera_trigger:
    num_samples: int
    num_frames: int
    frame_trigger_onsets_idx: object
    fps: int

def get_Camera_trigger(session: Session) -> Camera_trigger:
    AI_file = glob(os.path.join(session.file_path, "analog*"))[-1] # take the last file if there are multiple
    AI_data = np.fromfile(AI_file)

    camera_trigger_data = AI_data[np.arange(0, len(AI_data), 4)] # four interleaved time series

    camera_trigger_num_samples = len(camera_trigger_data)
    num_frames_expected, duration_of_video, frame_trigger_onsets_idx = get_num_frames_expected(session, camera_trigger_data)
    fps = get_fps(session, num_frames_expected, duration_of_video)

    camera_trigger = Camera_trigger(camera_trigger_num_samples, num_frames_expected, frame_trigger_onsets_idx, fps)

    return camera_trigger

def get_num_frames_expected(session: Session, camera_trigger_data: object) -> int:

    frame_trigger_onsets = np.diff(camera_trigger_data)
    frame_trigger_onsets_idx = np.where(frame_trigger_onsets > 1)[0] + 1
    num_frames_expected = len(frame_trigger_onsets_idx)

    duration_of_video = (frame_trigger_onsets_idx[-1] - frame_trigger_onsets_idx[0])/session.daq_sampling_rate

    return num_frames_expected, duration_of_video, frame_trigger_onsets_idx

def get_fps(session: Session, num_frames_expected: int, duration_of_video: int) -> int:

    fps = int(num_frames_expected / duration_of_video)

    return fps