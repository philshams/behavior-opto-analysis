import os
import dill as pickle

def open_tracking_data(self):
        assert os.path.isfile(self.session.video.tracking_data_file), 'Tracking data not found for session: {}'.format(self.session.name)
        with open(self.session.video.tracking_data_file, "rb") as dill_file: self.tracking_data = pickle.load(dill_file)

def index_onset_and_duration_by_stim_type(self):
        self.onset_frames = {}
        self.onset_frames['laser']  = self.session.laser.onset_frames
        self.onset_frames['audio']  = self.session.audio.onset_frames
        self.onset_frames['homing'] = self.session.homing.onset_frames
        self.stimulus_durations = {}
        self.stimulus_durations['laser']  = self.session.laser.stimulus_durations
        self.stimulus_durations['audio']  = self.session.audio.stimulus_durations
        self.stimulus_durations['homing'] = self.session.homing.stimulus_durations
        