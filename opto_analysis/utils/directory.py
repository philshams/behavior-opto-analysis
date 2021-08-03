import os
from pathlib import Path 

class Directory():
    def __init__(self, base_folder: str, experiment:str=None, stim_type: bool=False, tracking_video:bool=False):
        if stim_type=='audio': self.leaf_folder='escape videos'
        if stim_type=='laser': self.leaf_folder='laser videos'
        
        self.generate_directory_name(base_folder, experiment=experiment, stim_type=stim_type, tracking_video=tracking_video)
        self.create_directory()

    def generate_directory_name(self, base_folder: str, experiment:str=None, stim_type: bool=False, tracking_video:bool=False):
        if stim_type: 
            self.path = os.path.join(base_folder, "trial clips", experiment, self.leaf_folder)
        if tracking_video: 
            self.path = os.path.join(base_folder, "trial clips", "__tracking__")

    def create_directory(self):
        if os.path.isdir(self.path): return
        # os.mkdir(self.path)
        Path(self.path).mkdir(parents=True)


