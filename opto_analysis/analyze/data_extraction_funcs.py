from typing import Tuple
from opto_analysis.analyze.analysis_funcs import *

def initialize_trial_dict(self, trial_start_idx: int, trial_end_idx: int, epoch: str) -> dict:
    trial = {}
    trial['session count']  = self.session_count
    trial['trial count']  = self.trial_count
    trial['group number'] = self.group_num
    trial['epoch'] = epoch
    trial['trajectory x'] = self.tracking_data['avg_loc'][trial_start_idx:trial_end_idx, 0]
    trial['trajectory y'] = self.tracking_data['avg_loc'][trial_start_idx:trial_end_idx, 1]

    return trial

def get_trial_start_and_end(self, onset_frames: list, stim_durations: list, epoch: str) -> Tuple[int, int]:
    if epoch=='stimulus':
        trial_start_idx = onset_frames[0] 
        trial_end_idx = int(onset_frames[-1] + stim_durations[-1]*self.fps)
    if epoch=='post-laser':
        trial_start_idx = int(onset_frames[-1] + stim_durations[-1]*self.fps)
        trial_end_idx = trial_start_idx + self.fps * self.settings.post_laser_seconds_to_plot
    return trial_start_idx, trial_end_idx

def add_relevant_data_to_trial_dict(self, trial: dict, trial_start_idx: int, trial_end_idx: int, epoch: str):
    if'trajectories' in self.analysis_type:
        trial['trajectory y'] = self.session.video.rendering_size_pixels - trial['trajectory y']
        trial['speed'] = self.tracking_data['speed'][trial_start_idx+1:trial_end_idx]
        if epoch=='stimulus':   trial['linewidth'] = 3
        if epoch=='post-laser': trial['linewidth'] = 1
    if 'targets' in self.analysis_type:
        trial['escape initiation idx'] = get_escape_initiation_idx(self, trial_start_idx)
        trial['escape target score'] = get_escape_target_score(self, trial['trajectory x'], trial['trajectory y'], trial['escape initiation idx'])
    return trial