import dill as pickle
import numpy as np
from dataclasses import dataclass
from opto_analysis.utils.open_tracking_data import open_tracking_data
from opto_analysis.utils.get_onset_and_duration import get_onset_and_duration

@dataclass(frozen=True)
class Homings:
    onset_frames: object
    stimulus_durations: object
    fast_speed: float
    fast_anglular_speed: float
    padding_duration: float
    heading_dir_threshold_angle: int
    min_change_in_dist_to_shelter: int
    

class get_Homings:
    def __init__(self,session, settings):
        self.settings = settings
        self.session = session

        self.extract_variables()
        self.identify_homing_runs()
        self.get_onset_and_duration()
        self.remove_inapplicable_runs()

        self.session.homings = Homings(
                                self.onset_frames, 
                                self.stimulus_durations, 
                                self.settings.fast_speed, 
                                self.settings.fast_angluar_speed,
                                self.settings.padding_duration, 
                                self.settings.heading_dir_threshold_angle, 
                                self.settings.min_change_in_dist_to_shelter,
                                self.settings.threat_area_height,
                                self.settings.threat_area_width,
                                self.settings.subgoal_locations)
        self.save_session()

# --------MAIN FUNCS-----------------------------------------------
    def extract_variables(self):
        open_tracking_data(self) # generates self.tracking_data
        self.distance_from_shelter = self.tracking_data['distance rel. to shelter']
        self.homing_angle          = self.get_homing_angle()
        self.homing_speed_smoothed = self.get_homing_speed()
        self.homing_speed_angular  = self.get_homing_speed_angular()
        self.speed_along_y_axis    = self.get_speed_along_y_axis()

    def identify_homing_runs(self):
        facing_shelter_or_edge         = self.homing_angle          < self.settings.heading_dir_threshold_angle
        move_fast_to_shelter_or_edge   = self.homing_speed_smoothed > self.settings.fast_speed
        turn_fast_to_shelter_or_edge   = self.homing_speed_angular  > self.settings.fast_angular_speed
        move_at_all_to_shelter_or_edge = self.speed_along_y_axis    > 0
        turn_at_all_to_shelter_or_edge = self.homing_speed_angular  > 0

        go_fast_to_shelter_or_edge   = move_fast_to_shelter_or_edge * facing_shelter_or_edge + turn_fast_to_shelter_or_edge
        go_at_all_to_shelter_or_edge = move_at_all_to_shelter_or_edge + turn_at_all_to_shelter_or_edge

        go_fast_to_shelter_or_edge_padded = self.boxcar_filter(go_fast_to_shelter_or_edge, self.settings.padding_duration*self.session.video.fps, +1, time='current')

        self.homing_runs_on = (go_fast_to_shelter_or_edge_padded * go_at_all_to_shelter_or_edge).astype(bool)

    def get_onset_and_duration(self):
        self.onset_frames, self.stimulus_durations, self.offset_frames = \
            get_onset_and_duration(self.homing_runs_on, self.session, stim_type='spontaneous homings', min_frames_between_trials=1, round_durations=False)

    def remove_inapplicable_runs(self):
        change_in_distance_to_shelter = (self.distance_from_shelter[self.offset_frames] - self.distance_from_shelter[self.onset_frames]) / self.distance_from_shelter[self.onset_frames]
        homing_run_durations          = self.offset_frames - self.onset_frames
        start_loc_x                   = self.tracking_data['avg_loc'][self.onset_frames, 0]
        start_loc_y                   = self.tracking_data['avg_loc'][self.onset_frames, 1]

        sufficient_move_toward_shelter = change_in_distance_to_shelter >  self.settings.min_change_in_dist_to_shelter
        sufficient_run_duration        = homing_run_durations          > (self.settings.padding_duration * self.session.video.fps + 2)
        starts_in_threat_area          = (start_loc_y                  >  self.settings.threat_area_height) * \
        (abs(start_loc_x - self.session.video.rendering_size_pixels/2) >  self.settings.threat_area_width/2)

        applicable_runs         = sufficient_move_toward_shelter * sufficient_run_duration * starts_in_threat_area
        self.onset_frames       = self.onset_frames[applicable_runs]
        self.stimulus_durations = self.stimulus_durations[applicable_runs]

    def save_session(self):
        with open(self.session.metadata_file, "wb") as dill_file: pickle.dump(self.session, dill_file)

# --------DATA PROCESSING FUNCS---------------------------------------
    def boxcar_filter(self, data, filter_length, sign, time='current'):
        if time == 'past':
            filtered_data = np.concatenate((np.zeros(filter_length - 1), np.convolve(data, np.ones(filter_length) * sign, mode='valid'))) / filter_length
        if time == 'future':
            filtered_data = np.concatenate((np.convolve(data, np.ones(filter_length) * sign, mode='valid'), np.zeros(filter_length - 1))) / filter_length
        if time == 'current':
            filtered_data = np.concatenate((np.zeros(int(filter_length/2 - 1)), np.convolve(data, np.ones(filter_length) * sign, mode='valid'), np.zeros(int(filter_length/2)))) / filter_length
        return filtered_data

    def get_homing_angle(self):
        pass

    def get_homing_speed(self):
        pass
    
    def get_homing_speed_angular(self):
        pass
    
    def get_speed_along_y_axis(self):
        pass
    

