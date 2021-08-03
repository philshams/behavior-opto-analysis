import numpy as np
from typing import Tuple

def trial_is_eligible(self, onset_frames: list) -> bool:
    eligible = self.stim_type=='audio' and \
                successful_escape(self, onset_frames) and \
                self.num_successful_escapes_this_session <  self.settings.max_num_trials            
    if eligible: self.num_successful_escapes_this_session += 1
    return eligible

def successful_escape(self, onset_frames: list) -> bool:
    if self.tracking_data['distance rel. to shelter'][onset_frames[0]] < self.settings.min_distance_from_shelter*10: return False

    location_during_threat = self.tracking_data['avg_loc'][onset_frames[0]:onset_frames[0]+self.fps*self.settings.max_escape_duration, :]
    distance_from_shelter_during_threat = ((location_during_threat[:,0]-self.session.video.shelter_location[0])**2 + \
                                            (location_during_threat[:,1]-self.session.video.shelter_location[1])**2)**.5
    successful_escape = (distance_from_shelter_during_threat < self.settings.min_distance_from_shelter*10).any()
    return successful_escape

def get_escape_initiation_idx(self, trial_start_idx: int) -> int:
    escape_initiation_idx = np.where(self.tracking_data['speed rel. to shelter'][trial_start_idx+1:] > self.settings.escape_initiation_speed)[0][0]
    assert escape_initiation_idx < (self.settings.max_escape_duration*self.fps)
        # print("Escape initiation taking longer than max escape duration, session: {}, at time: {} min".format(self.session.name, np.round(trial_start_idx/self.fps/60, 2)))
        # return None # escape initiation time is longer than max escape duration
    return escape_initiation_idx

def get_escape_target_score(self, x: np.ndarray, y: np.ndarray, RT: int) -> float:
    y_start, x_start = y[RT], x[RT]
    y_goal, x_goal   = self.session.video.shelter_location[1], self.session.video.shelter_location[0]
    y_target         = 512 - 100 # 10cm in front of the wall
    x_target         = x[np.argmin(abs(y-y_target))]
    y_obstacle_edge  = 512
    x_obstacle_edge  = 512 + np.sign(x[np.argmin(abs(y-y_obstacle_edge))]-512) * 250

    distance_path_to_homing_vector, _           = distance_to_line(x_target, y_target, x_start, y_start, x_goal, y_goal)
    distance_path_to_edge_vector, x_edge_vector = distance_to_line(x_target, y_target, x_start, y_start, x_obstacle_edge, y_obstacle_edge)
    distance_edge_vector_to_homing_vector, _    = distance_to_line(x_edge_vector, y_target, x_start, y_start, x_goal, y_goal)

    escape_target_score = abs(distance_path_to_homing_vector - distance_path_to_edge_vector + distance_edge_vector_to_homing_vector) / (2*distance_edge_vector_to_homing_vector)
    return escape_target_score

def distance_to_line(x, y, x_start, y_start, x_goal, y_goal) -> Tuple[float, float]:
    slope = (y_goal - y_start) / (x_goal - x_start)
    intercept = y_start - x_start * slope
    distance_of_path_to_line = abs(y - slope * x - intercept) / np.sqrt((-slope) ** 2 + (1) ** 2)
    x_pos_at_y_value = (y - intercept) / slope
    return distance_of_path_to_line, x_pos_at_y_value