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
        self.session_counter = -1
        self.trial_counter = 0

    def trajectories(self, stim_type):
        for session_ID in self.session_IDs:
            self.load_session_for_plotting(session_ID) 
            self.initialize_plotting_parameters(stim_type) 
            self.open_its_tracking_data()
            self.plot_arena()
            self.select_trials_to_plot()
            self.plot_trial_trajectories()
        self.save_plot()

# ----FIRST-ORDER PLOTTING FUNCS-----------------------------------------

    def load_session_for_plotting(self, session_ID):
        self.session = Process(session_ID).load_session()

    def initialize_plotting_parameters(self, stim_type):
        self.stim_type = stim_type
        self.fps = self.session.video.fps
        self.session_counter += 1

    def open_its_tracking_data(self):
        open_tracking_data(self)

    def plot_arena(self):
        if not self.arena_already_plotted:
            self.arena_already_plotted = True
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

            plt.axis('off')
            self.ax.margins(0, 0)
            self.ax.xaxis.set_major_locator(plt.NullLocator())
            self.ax.yaxis.set_major_locator(plt.NullLocator())

    def select_trials_to_plot(self):
        self.trials_to_plot = []
        for onset_frames, stim_durations in zip(self.session.__dict__[self.stim_type].onset_frames, \
                                                self.session.__dict__[self.stim_type].stimulus_durations):
            self.trial_counter+=1
            trial_start_idx = onset_frames[0] 
            trial_end_idx = int(onset_frames[-1] + stim_durations[-1]*self.fps)
            size = self.session.video.rendering_size_pixels
            self.create_trial_dict(trial_start_idx, trial_end_idx, size, epoch='stimulus')
            if self.stim_type=='laser':
                trial_start_idx = int(onset_frames[-1] + stim_durations[-1]*self.fps)
                distance_from_trial_start = \
                  ((self.tracking_data['avg_loc'][trial_start_idx:,0] - self.tracking_data['avg_loc'][trial_start_idx,0])**2 +\
                   (self.tracking_data['avg_loc'][trial_start_idx:,1] - self.tracking_data['avg_loc'][trial_start_idx,1])**2)**.5
                trial_end_idx = trial_start_idx + np.where(distance_from_trial_start>200)[0][0]
                self.create_trial_dict(trial_start_idx, trial_end_idx, size, epoch='post-laser')
        # TODO: determine trial eligibility (audio trials: under max escapes per mouse, under max time to reach shelter)

    def plot_trial_trajectories(self):
        for trial in self.trials_to_plot:
            self.update_color_counter(trial['trial_count'])
            if self.settings.color_by in ['speed', 'time']: 
                self.colorline(trial['trajectory_x'], trial['trajectory_y'], trial['speed'], trial['epoch'], trial['linewidth'])
                continue
            self.line(trial['trajectory_x'], trial['trajectory_y'], trial['epoch'], trial['linewidth'])
            
    def save_plot(self):
        # plt.ion()
        plt.show()
        file_base_name = os.path.join(self.settings.save_folder, self.session.experiment, self.settings.analysis.title)
        file_extension = '.png'
        file_suffix = ''
        if self.settings.color_by: 
            file_suffix = '_color by ' + self.settings.color_by
        self.fig.savefig(file_base_name+file_suffix+file_extension, bbox_inches='tight', pad_inches=0)

# ----PLOTTING HELPER FUNCS-----------------------------------------------------

    def line(self, x: np.ndarray, y: np.ndarray, epoch: str, linewidth: int, color: tuple=(.4,.4,.4, .7)):
        if self.settings.color_by:
            color = get_colormap(object_to_color='plot', epoch=epoch)[self.color_counter%16]
        self.ax.plot(x, y, color = color, linewidth=linewidth)

    def colorline(self, x: np.ndarray, y: np.ndarray, speeds: np.ndarray, epoch: str, linewidth: int):
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        colors = generate_list_of_colors(self.settings.color_by, self.stim_type, epoch, speeds)
        set_of_lines = plt_coll.LineCollection(segments, colors=colors, linewidth=linewidth)
        self.ax.add_collection(set_of_lines)

    def create_trial_dict(self, trial_start_idx: int, trial_end_idx: int, size: int, epoch: str='stimulus'):
        trial = {}
        trial['trajectory_x'] = self.tracking_data['avg_loc'][trial_start_idx:trial_end_idx, 0]
        trial['trajectory_y'] = size - self.tracking_data['avg_loc'][trial_start_idx:trial_end_idx, 1]
        trial['speed'] = self.tracking_data['speed'][trial_start_idx+1:trial_end_idx]
        trial['epoch'] = epoch
        trial['trial_count'] = self.trial_counter
        if epoch=='stimulus':   trial['linewidth'] = 3
        if epoch=='post-laser': trial['linewidth'] = 1
        self.trials_to_plot.append(trial)
        
    def update_color_counter(self, trial_count):
        if self.settings.color_by=='trial':   self.color_counter = trial_count
        if self.settings.color_by=='session': self.color_counter = self.session_counter
