from tokenize import group
from typing import Tuple
from opto_analysis.process.process import Process
from opto_analysis.utils.open_tracking_data import open_tracking_data
from opto_analysis.utils.color_funcs import get_color_based_on_speed, get_colormap, generate_list_of_colors
import matplotlib.pyplot as plt
import matplotlib.collections as plt_coll
import numpy as np
import os

class Analyze():
    def __init__(self, session_IDs, settings, analysis_type):
        self.settings = settings
        self.session_IDs = session_IDs
        self.session_count = -1
        self.trial_count = 0
        self.data_x = np.array([])
        self.data_y = np.array([])
        self.trial_colors   = []
        self.trials_to_plot = []
        self.group_nums = np.unique(session_IDs[:, 5])
        self.num_of_groups = np.ptp(self.group_nums)+1       
        self.analysis_type = analysis_type
        if analysis_type=='escape trajectories': self.stim_type='audio'
        if analysis_type=='escape targets':      self.stim_type='audio'
        if analysis_type=='laser trajectories':  self.stim_type='laser'

    def plot(self):
        self.initialize_figure()
        for session_ID in self.session_IDs:
            self.load_session_for_plotting(session_ID) 
            self.initialize_session_parameters() 
            self.open_its_tracking_data()
            self.extract_data_from_each_trial()
        self.plot_data()
        self.save_plot()

# ----FIRST-ORDER PLOTTING FUNCS-----------------------------------------

    def initialize_figure(self):
        self.load_session_for_plotting(self.session_IDs[0]) 
        if 'trajectories' in self.analysis_type: self.initialize_arena_plot()
        if 'targets' in self.analysis_type:      self.initialize_box_plot()
        plt.axis('off')
        self.ax.margins(0, 0)
        self.ax.xaxis.set_major_locator(plt.NullLocator())
        self.ax.yaxis.set_major_locator(plt.NullLocator())

    def load_session_for_plotting(self, session_ID):
        self.session = Process(session_ID).load_session()
        self.group_num = session_ID[5]

    def initialize_session_parameters(self):
        self.fps = self.session.video.fps
        self.session_count += 1
        self.num_successful_escapes_this_session = 0

    def open_its_tracking_data(self):
        open_tracking_data(self)

    def extract_data_from_each_trial(self):
        for onset_frames, stim_durations in zip(self.session.__dict__[self.stim_type].onset_frames, \
                                                self.session.__dict__[self.stim_type].stimulus_durations):
            if not self.trial_is_eligible(onset_frames): continue
            self.generate_trial_dict(onset_frames, stim_durations, epoch='stimulus')
            self.generate_trial_dict(onset_frames, stim_durations, epoch='post-laser')
            self.trial_count+=1

    def plot_data(self):
        if 'trajectories' in self.analysis_type:
            for trial in self.trials_to_plot:
                if self.settings.color_by in ['speed', 'time']: 
                    self.gradient_line(trial)
                else:
                    self.solid_line(trial)
        if 'targets' in self.analysis_type:
            for trial in self.trials_to_plot:
                self.data_x =  np.append(self.data_x, trial['group number'])
                self.data_y =  np.append(self.data_y, trial['escape target score'])
                self.trial_colors.append(self.get_solid_color(trial, plot_type='scatter'))
            self.plot_box_plot()
            self.plot_scatter_data()
                    
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
        self.fig.canvas.set_window_title(self.settings.analysis.title) 
        circle = plt.Circle((size/2, size/2), radius=460, color=[0, 0, 0], linewidth=1, fill=False)
        self.ax.add_artist(circle)

    def initialize_box_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(self.num_of_groups*2, 9))
        self.fig.canvas.set_window_title(self.settings.analysis.title) 
        self.fig.tight_layout()
        self.ax.set_ylim([-.05, 1.05])
        self.x_range = [min(self.group_nums)-.6, max(self.group_nums)+.6]
        self.ax.set_xlim(self.x_range)
        plt.plot(self.x_range, [0,0],     color=(.9,.9,.9), linestyle='--', zorder=-1)
        plt.plot(self.x_range, [1,1],     color=(.9,.9,.9), linestyle='--', zorder=-1)
        plt.plot(self.x_range, [.65,.65], color=(.9,.9,.9), linestyle='--', zorder=-1)

    def plot_scatter_data(self):
        self.apply_x_jitter(offset_x=0, min_distance_y=0.01, jitter_distance_x=0.02 * self.num_of_groups)
        self.ax.scatter(self.jittered_data_x, self.data_y, color=self.trial_colors, linewidth=0, s=35, zorder=99)

    def plot_box_plot(self, width=.4):
        for group_num in self.group_nums:
            group_data_y = self.data_y[self.data_x==group_num]
            quartile_1, median, quartile_3 = np.percentile(group_data_y, [25, 50, 75])
            iqr = quartile_3 - quartile_1
            lower_range = max(min(group_data_y), quartile_1-1.5*iqr)
            upper_range = min(max(group_data_y), quartile_3+1.5*iqr)
            color = (.9,.9,.9)

            whiskers = self.ax.plot([group_num,group_num], [lower_range, upper_range], color=color, linewidth=10)
            boxplot = plt.Rectangle((group_num-width/2, quartile_1), width, iqr, color=color, edgecolor=None, fill=True)
            self.ax.add_artist(boxplot)

            median_line = self.ax.plot([group_num-width/2.1, group_num+width/2.05], [median, median], color=(0,0,0), linewidth=1.5)

    def solid_line(self, trial: dict):
        color = self.get_solid_color(trial, plot_type='trajectory')
        self.ax.plot(trial['trajectory x'], trial['trajectory y'], color = color, linewidth=trial['linewidth'])

    def get_solid_color(self, trial: dict, plot_type:str='trajectory') -> tuple:
        if not self.settings.color_by: 
            color=(.4,.4,.4, .7)
            return color
        if self.settings.color_by=='target': 
            if trial['escape target score'] >  self.settings.edge_vector_threshold: color = (0, .4, 1, .6)
            if trial['escape target score'] <= self.settings.edge_vector_threshold: color = (.4,.4,.4,  1)
            return color
        if self.settings.color_by=='trial':      self.color_counter = trial['trial count']
        if self.settings.color_by=='session':    self.color_counter = trial['session count']
        color = get_colormap(object_to_color='plot', epoch=trial['epoch'], plot_type=plot_type)[self.color_counter%16]
        return color

    def gradient_line(self, trial: dict):
        points = np.array([trial['trajectory x'], trial['trajectory y']]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        colors = generate_list_of_colors(self.settings.color_by, self.stim_type, trial['epoch'], trial['speed'])
        set_of_lines = plt_coll.LineCollection(segments, colors=colors, linewidth=trial['linewidth'])
        self.ax.add_collection(set_of_lines)

    def apply_x_jitter(self, offset_x=.35, min_distance_y=0.01, jitter_distance_x=0.04):
        data_x = self.data_x.copy()
        if self.settings.x_jitter:
            all_points_adequately_separated = False
            sign_inverter = -1
            multiplier = 1
            while not all_points_adequately_separated:
                all_points_adequately_separated=True
                for round in ['do jitter', 'test separation']:
                    for i, data_point_y in enumerate(self.data_y):
                        all_but_this_point_idx      = np.arange(len(self.data_y))!=i
                        y_distances                 = abs(data_point_y - self.data_y[all_but_this_point_idx])
                        y_close_points_idx          = np.where(y_distances < min_distance_y)[0]
                        x_distances_of_close_points = abs(data_x[i] - data_x[all_but_this_point_idx][y_close_points_idx])
                        x_close_points_idx          = np.where(np.round(x_distances_of_close_points,2) < np.round(jitter_distance_x*2,2))[0]
                        if y_close_points_idx.size and x_close_points_idx.size:
                            if round=='do jitter':
                                sign = np.sign(np.mean(data_x[all_but_this_point_idx][y_close_points_idx][x_close_points_idx])+.001) * sign_inverter
                                data_x[i] += sign*jitter_distance_x*multiplier
                            if round=='test separation':
                                all_points_adequately_separated=False
                sign_inverter = 1
                multiplier = 2
        self.jittered_data_x = data_x+offset_x

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

    def generate_trial_dict(self, onset_frames: list, stim_durations: list, epoch: str='stimulus'):
        if epoch=='post-laser' and self.stim_type=='audio': return
        trial, trial_start_idx, trial_end_idx = self.initialize_trial_dict(onset_frames, stim_durations, epoch)
        if'trajectories' in self.analysis_type:
            trial['trajectory y'] = self.session.video.rendering_size_pixels - trial['trajectory y']
            trial['speed'] = self.tracking_data['speed'][trial_start_idx+1:trial_end_idx]
            if epoch=='stimulus':   trial['linewidth'] = 3
            if epoch=='post-laser': trial['linewidth'] = 1
        if 'targets' in self.analysis_type:
            trial['escape initiation idx'] = self.get_escape_initiation_idx(trial_start_idx)
            trial['escape target score'] = 1 - 1.5 * self.get_escape_target_score(trial['trajectory x'], trial['trajectory y'], trial['escape initiation idx']) #temp!!
        self.trials_to_plot.append(trial)

    def initialize_trial_dict(self, onset_frames: list, stim_durations: list, epoch: str) -> Tuple[int, int]:
        if epoch=='stimulus':
            trial_start_idx = onset_frames[0] 
            trial_end_idx = int(onset_frames[-1] + stim_durations[-1]*self.fps)
        if epoch=='post-laser':
            trial_start_idx = int(onset_frames[-1] + stim_durations[-1]*self.fps)
            trial_end_idx = trial_start_idx + self.fps * self.settings.post_laser_seconds_to_plot
        trial = {}
        trial['session count']  = self.session_count
        trial['trial count']  = self.trial_count
        trial['group number'] = self.group_num
        trial['epoch'] = epoch
        trial['trajectory x'] = self.tracking_data['avg_loc'][trial_start_idx:trial_end_idx, 0]
        trial['trajectory y'] = self.tracking_data['avg_loc'][trial_start_idx:trial_end_idx, 1]

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