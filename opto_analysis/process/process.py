from opto_analysis.process.session import Session, get_Session
from opto_analysis.process.camera_trigger import get_Camera_trigger
from opto_analysis.process.laser import get_Laser
from opto_analysis.process.audio import get_Audio
from opto_analysis.process.video import get_Video
import os
import numpy as np
import dill as pickle

class Process():
    def __init__(self, session_ID):
        self.session = get_Session(session_ID)

    def create_session(self, settings) -> Session:        
        self.load_registration_transform()
        self.session.camera_trigger = get_Camera_trigger(self.session)
        self.session.laser          = get_Laser(self.session)
        self.session.audio          = get_Audio(self.session)
        self.session.video          = get_Video(self.session, settings, self.loaded_registration_transform)
        self.print_session_details()
        self.save_session()
        self.verify_all_frames_saved()
        self.verify_aligned_data_streams()
        return self.session

    def save_session(self, overwrite=True):
        assert not os.path.isfile(self.session.metadata_file) or overwrite, "Permission to save not granted"
        with open(self.session.metadata_file, "wb") as dill_file: pickle.dump(self.session, dill_file)

    def load_session(self) -> Session:
        with open(self.session.metadata_file, "rb") as dill_file: session = pickle.load(dill_file)
        return session

    def load_registration_transform(self) -> object:
        if os.path.isfile(self.session.metadata_file) and isinstance(self.load_session().video.registration_transform, np.ndarray):
            self.loaded_registration_transform = self.load_session().video.registration_transform
        else: self.loaded_registration_transform = None

    def print_session_details(self):
        for key in self.session.__dict__.keys():
            if key in ['name','number','mouse','date','experiment','previous_sessions']:
                print(" {}: {}".format(key, self.session.__dict__[key]))
            elif key in ['camera_trigger', 'laser','audio','video']:
                if key == 'camera_trigger': print("")
                print(" {} metadata saved".format(key))
        print(" registration transform: {}".format(isinstance(self.session.video.registration_transform, np.ndarray)))
        print(" -----------------")

    def verify_all_frames_saved(self):
        assert self.session.camera_trigger.num_frames == self.session.video.num_frames, "---Video contains {} frames, but {} frames were triggered! (for experiment: {}, mouse: {})---".format(self.session.camera_trigger.num_frames, self.session.video.num_frames, self.session.experiment, self.session.mouse)

    def verify_aligned_data_streams(self, known_offset: int = 6000) -> None:
        assert self.session.camera_trigger.num_samples == self.session.audio.num_samples and self.session.camera_trigger.num_samples == (self.session.laser.num_samples+known_offset), "---Data streams have mismatched numbers of samples---\nCamera trigger: {}\nAudio input: {}\nLaser output: {} = {} + {}".format(self.session.camera_trigger.num_samples, self.session.audio.num_samples, (self.session.laser.num_samples+known_offset), self.session.laser.num_samples, known_offset)