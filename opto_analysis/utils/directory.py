import os
from pathlib import Path 

class Directory():
    def __init__(self, base_folder: str, experiment:str=None, analysis_type: str=None, stim_type: bool=False, tracking_video:bool=False, plot: bool=False):
        if stim_type=='audio':              self.leaf_folder='escape videos'
        if stim_type=='laser':              self.leaf_folder='laser videos'
        if stim_type=='homing':             self.leaf_folder='homing videos'
        if stim_type=='threshold_crossing': self.leaf_folder='threshold crossing videos'
        self.base_folder    = base_folder
        self.experiment     = experiment
        self.analysis_type  = analysis_type
        self.stim_video     = stim_type
        self.tracking_video = tracking_video
        self.plot           = plot
        self.generate_directory_name()
        self.create_directory()

    def generate_directory_name(self):
        if self.stim_video: 
            self.path = os.path.join(self.base_folder, self.experiment, self.leaf_folder)
        if self.tracking_video: 
            self.path = os.path.join(self.base_folder, "__tracking__", self.leaf_folder)
        if self.plot:
            self.path = os.path.join(self.base_folder, self.analysis_type)

    def create_directory(self):
        if os.path.isdir(self.path): return
        Path(self.path).mkdir(parents=True)

    def file_name(self, mouse: str=None, trial_num: int=None, minutes_into_session: int=None, title: str=None, color_by: str=None, plot_extension: str = '.png') -> str:
        if self.stim_video or self.tracking_video:
            self.file_name = os.path.join(self.path,"{}-{} ({}').mp4".format(mouse, trial_num, minutes_into_session))
        if self.plot:
            if color_by: color_by_text = '_color=' + color_by
            else       : color_by_text = ''
            self.file_name = os.path.join(self.path, title + color_by_text + plot_extension)
        return self.file_name