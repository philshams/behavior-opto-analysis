from typing import Tuple
from opto_analysis.process.process import Process
from opto_analysis.utils.open_tracking_data import open_tracking_data
from opto_analysis.utils.color_funcs import get_color_based_on_speed, get_colormap, generate_list_of_colors
import matplotlib.pyplot as plt
import matplotlib.collections as plt_coll
import numpy as np
import os

class Analyze():
    def __init__(self, session_IDs, settings):
        self.settings = settings
        self.session_IDs = session_IDs
        self.arena_already_plotted = False
        self.session_count = -1
        self.trial_count = 0

    def plot(self, plot_type):
        for session_ID in self.session_IDs:
            self.load_session_for_plotting(session_ID) 
            self.initialize_plotting_parameters(plot_type) 
            self.open_its_tracking_data()
            self.initialize_figure()
            self.extract_data_from_each_trial()
            self.plot_trial_data()
        self.save_plot()


# ----FIRST-ORDER PLOTTING FUNCS-----------------------------------------

    def load_session_for_plotting(self, session_ID):
        self.session = Process(session_ID).load_session()

    def initialize_plotting_parameters(self, plot_type):
        self.fps = self.session.video.fps
        self.session_count += 1
        self.num_successful_escapes_this_session = 0
        self.plot_type = plot_type
        if plot_type=='escape trajectories':
            self.stim_type='audio'
            self.data_type='trajectory'
        if plot_type=='laser trajectories':
            self.stim_type='laser'
            self.data_type='trajectory'
        if plot_type=='escape targets':
            self.stim_type='audio'
            self.data_type='distribution'

    def open_its_tracking_data(self):
        open_tracking_data(self)

    def initialize_figure(self):
        if self.arena_already_plotted: return
        if self.data_type=='trajectory':   self.initialize_arena_plot()
        if self.data_type=='distribution': self.initialize_box_plot()
        plt.axis('off')
        self.ax.margins(0, 0)
        self.ax.xaxis.set_major_locator(plt.NullLocator())
        self.ax.yaxis.set_major_locator(plt.NullLocator())
        self.arena_already_plotted = True

    def extract_data_from_each_trial(self):
        self.trials_to_plot = []
        for onset_frames, stim_durations in zip(self.session.__dict__[self.stim_type].onset_frames, \
                                                self.session.__dict__[self.stim_type].stimulus_durations):
            if not self.trial_is_eligible(onset_frames): continue
            self.create_trial_dict(onset_frames, stim_durations, epoch='stimulus')
            self.create_trial_dict(onset_frames, stim_durations, epoch='post-laser')
            self.trial_count+=1

    def plot_trial_data(self):
        if self.data_type=='trajectory':
            for trial in self.trials_to_plot:
                if self.settings.color_by in ['speed', 'time']: self.colorline(trial)
                else: self.line(trial)
        if self.plot_type=='escape targets':
            for trial in self.trials_to_plot:
                print(trial['escape initiation idx'])
                print(trial['escape target score'])
                print('')
                
    def save_plot(self):
        # plt.ion()
        plt.show()
        file_base_name = os.path.join(self.settings.save_folder, self.session.experiment, "plots", self.settings.analysis.title)
        file_extension = '.png'
        file_suffix = ''
        if self.settings.color_by: 
            file_suffix = '_color by ' + self.settings.color_by
        self.fig.savefig(file_base_name+file_suffix+file_extension, bbox_inches='tight', pad_inches=0)

# ----PLOTTING HELPER FUNCS----------------------------------------------

    def initialize_arena_plot(self):
        size = self.session.video.rendering_size_pixels
        if self.stim_type=='audio':
            self.fig, self.ax = plt.subplots(figsize=(9,9))
            self.ax.set_xlim([0, size])
            self.ax.set_ylim([0, size])
        if self.stim_type=='laser': 
            self.fig, self.ax = plt.subplots(figsize=(4.5,9))
            self.ax.plot([size/2-250, size/2+250], [size/2, size/2], color=[0, 0, 0], linewidth=5) #obstacle
            self.ax.set_xlim([0, size/2])
            self.ax.set_ylim([0, size])   
        circle = plt.Circle((size/2, size/2), radius=460, color=[0, 0, 0], linewidth=1, fill=False)
        self.ax.add_artist(circle)

    def initialize_box_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(9, 9))
        self.ax.set_ylim([-.05, 1.19])

    def line(self, trial: dict, color: tuple=(.4,.4,.4, .7)):
        if self.settings.color_by:
            self.update_color_counter(trial['trial_count'])
            color = get_colormap(object_to_color='plot', epoch=trial['epoch'])[self.color_counter%16]
        self.ax.plot(trial['trajectory_x'], trial['trajectory_y'], color = color, linewidth=trial['linewidth'])

    def colorline(self, trial: dict):
        points = np.array([trial['trajectory_x'], trial['trajectory_y']]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        colors = generate_list_of_colors(self.settings.color_by, self.stim_type, trial['epoch'], trial['speed'])
        set_of_lines = plt_coll.LineCollection(segments, colors=colors, linewidth=trial['linewidth'])
        self.ax.add_collection(set_of_lines)

    def create_trial_dict(self, onset_frames: list, stim_durations: list, epoch: str='stimulus'):
        if epoch=='post-laser' and self.stim_type=='audio': return
        trial, trial_start_idx, trial_end_idx = self.initialize_trial_dict(onset_frames, stim_durations, epoch)
        if self.data_type=='trajectory':
            trial['trajectory_y'] = self.session.video.rendering_size_pixels - trial['trajectory_y']
            trial['speed'] = self.tracking_data['speed'][trial_start_idx+1:trial_end_idx]
            trial['epoch'] = epoch
            if epoch=='stimulus':   trial['linewidth'] = 3
            if epoch=='post-laser': trial['linewidth'] = 1
        if self.plot_type=='escape targets':
            trial['escape initiation idx'] = self.get_escape_initiation_idx(trial_start_idx)
            trial['escape target score'] = self.get_escape_target_score(trial['trajectory_x'], trial['trajectory_y'], trial['escape initiation idx'])
        self.trials_to_plot.append(trial)

    def update_color_counter(self, trial_count):
        if self.settings.color_by=='trial':   self.color_counter = trial_count
        if self.settings.color_by=='session': self.color_counter = self.session_count

# ----ANALYSIS HELPER FUNCS----------------------------------------------

    def trial_is_eligible(self, onset_frames: list) -> bool:
        eligible = self.stim_type=='audio' and self.successful_escape(onset_frames) and \
                   self.num_successful_escapes_this_session <  self.settings.max_num_trials            
        if eligible: self.num_successful_escapes_this_session += 1
        return eligible

    def successful_escape(self, onset_frames: list) -> bool:
        location_during_threat = self.tracking_data['avg_loc'][onset_frames[0]:onset_frames[0]+self.fps*self.settings.max_escape_duration, :]

        distance_from_shelter_during_threat = ((location_during_threat[:,0]-self.session.video.shelter_location[0])**2 + \
                                               (location_during_threat[:,1]-self.session.video.shelter_location[1])**2)**.5

        successful_escape = (distance_from_shelter_during_threat < self.settings.min_distance_from_shelter*10).any()
        return successful_escape

    def initialize_trial_dict(self, onset_frames: list, stim_durations: list, epoch: str) -> Tuple[int, int]:
        if epoch=='stimulus':
            trial_start_idx = onset_frames[0] 
            trial_end_idx = int(onset_frames[-1] + stim_durations[-1]*self.fps)
        if epoch=='post-laser':
            trial_start_idx = int(onset_frames[-1] + stim_durations[-1]*self.fps)
            trial_end_idx = trial_start_idx + self.fps * self.settings.post_laser_seconds_to_plot

        trial = {}
        trial['trial_count'] = self.trial_count
        trial['trajectory_x'] = self.tracking_data['avg_loc'][trial_start_idx:trial_end_idx, 0]
        trial['trajectory_y'] = self.tracking_data['avg_loc'][trial_start_idx:trial_end_idx, 1]

        return trial, trial_start_idx, trial_end_idx

    def get_escape_initiation_idx(self, trial_start_idx: int):
        escape_initiation_idx = np.where(self.tracking_data['speed rel. to shelter'][trial_start_idx+1:] > self.settings.escape_initiation_speed)[0][0]
        assert escape_initiation_idx < (self.settings.max_escape_duration*self.fps), "escape initiation time is longer than max escape duration"
        return escape_initiation_idx

    def get_escape_target_score(self, x: np.ndarray, y: np.ndarray, RT: int) -> float:
        y_start, x_start = y[RT], x[RT]
        y_goal, x_goal   = self.session.video.shelter_location[1], self.session.video.shelter_location[0]
        y_target         = 512 - 100 # 10cm in front of the wall
        x_target         = x[np.argmin(abs(y-y_target))]
        y_obstacle_edge  = 512
        x_obstacle_edge  = 512 + np.sign(x[np.argmin(abs(y-y_obstacle_edge))]-512) * 250

        distance_path_to_homing_vector, _           = self.distance_to_line(x_target, y_target, x_start, y_start, x_goal, y_goal)
        distance_path_to_edge_vector, x_edge_vector = self.distance_to_line(x_target, y_target, x_start, y_start, x_obstacle_edge, y_obstacle_edge)
        distance_edge_vector_to_homing_vector, _    = self.distance_to_line(x_edge_vector, y_target, x_start, y_start, x_goal, y_goal)

        escape_target_score = abs(distance_path_to_homing_vector - distance_path_to_edge_vector + distance_edge_vector_to_homing_vector) / (2*distance_edge_vector_to_homing_vector)

        return escape_target_score

    def distance_to_line(self, x, y, x_start, y_start, x_goal, y_goal):
        slope = (y_goal - y_start) / (x_goal - x_start)
        intercept = y_start - x_start * slope
        distance_of_path_to_line = abs(y - slope * x - intercept) / np.sqrt((-slope) ** 2 + (1) ** 2)
        x_pos_at_y_value = (y - intercept) / slope
        return distance_of_path_to_line, x_pos_at_y_value