from opto_analysis.process.process import Process
from opto_analysis.utils.open_tracking_data import open_tracking_data
from opto_analysis.utils.color_funcs import get_color_based_on_speed, custom_colormap
import matplotlib.pyplot as plt
import matplotlib.collections as plt_coll
import numpy as np
import os

class Analyze():
    def __init__(self, session_IDs, settings):
        self.settings = settings
        self.session_IDs = session_IDs
        self.arena_already_plotted = False
        self.i = -1

    def trajectories(self, stim_type):
        for session_ID in self.session_IDs:
            self.load_session_for_plotting(session_ID)  
            self.open_its_tracking_data()
            self.plot_arena(stim_type)
            self.select_trials_to_plot(stim_type)
            self.plot_trial_trajectories()
        self.save_plot()

# ---------------------------------------------------------

    def load_session_for_plotting(self, session_ID):
        self.session = Process(session_ID).load_session()
        self.i += 1

    def open_its_tracking_data(self):
        open_tracking_data(self)

    def plot_arena(self, stim_type):
        if not self.arena_already_plotted:
            self.fig, self.ax = plt.subplots(figsize=(9,9))
            plt.axis('off')
            self.ax.margins(0, 0)
            self.ax.xaxis.set_major_locator(plt.NullLocator())
            self.ax.yaxis.set_major_locator(plt.NullLocator())

            size = self.session.video.rendering_size_pixels
            self.ax.set_xlim([0, size])
            self.ax.set_ylim([0, size])
            circle = plt.Circle((size/2, size/2), radius=460, color=[0, 0, 0], linewidth=1, fill=False)
            self.ax.add_artist(circle)
            if stim_type=='laser': self.ax.plot([25, 75], [50, 50], color=[0, 0, 0], linewidth=3) #obstacle
            self.arena_already_plotted = True

    def select_trials_to_plot(self, stim_type):
        self.trials_to_plot = []
        for onset_frames, stim_durations in zip(self.session.__dict__[stim_type].onset_frames, \
                                                self.session.__dict__[stim_type].stimulus_durations):
            trial_start_idx = onset_frames[0]
            trial_end_idx = int(onset_frames[-1] + stim_durations[-1]*self.session.video.fps)
            size = self.session.video.rendering_size_pixels
            trial = {}
            trial['trajectory_x'] = self.tracking_data['avg_loc'][trial_start_idx:trial_end_idx, 0]
            trial['trajectory_y'] = size - self.tracking_data['avg_loc'][trial_start_idx:trial_end_idx, 1]
            trial['speed'] = self.tracking_data['speed'][trial_start_idx+1:trial_end_idx]
            trial['stim_type'] = stim_type

            self.trials_to_plot.append(trial)
        # TODO: determine trial eligibility (audio trials: under max escapes per mouse, under max time to reach shelter)
        # TODO: laser trials

    def plot_trial_trajectories(self):
        for trial in self.trials_to_plot:
            if self.settings.color_by == 'speed':
                self.colorline(trial['trajectory_x'], trial['trajectory_y'], trial['speed'], trial['stim_type'])
            else:
                self.line(trial['trajectory_x'], trial['trajectory_y'], trial['stim_type'])

            
    def save_plot(self):
        # plt.ion()
        plt.show()
        file_base_name = os.path.join(self.settings.save_folder, self.session.experiment, self.settings.analysis.title)
        file_extension = '.png'
        file_suffix = ''
        if self.settings.color_by in ['speed','mouse','session']: 
            file_suffix = '_color by ' + self.settings.color_by
        self.fig.savefig(file_base_name+file_suffix+file_extension, bbox_inches='tight', pad_inches=0)

# ---------------------------------------------------------

    def line(self, x: np.ndarray, y: np.ndarray, stim_type: str, color: tuple=(.4,.4,.4), alpha: float=0.7):
        if self.settings.color_by=='mouse' or self.settings.color_by=='session':
            color = custom_colormap(object_to_color='plot')[self.i%10]
            alpha = 0.5
        self.ax.plot(x, y, color = color, linewidth=2, alpha=alpha)

    def colorline(self, x: np.ndarray, y: np.ndarray, speeds: np.ndarray, stim_type: str):
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        colors = []
        for speed in speeds:
            color = get_color_based_on_speed(speed=speed, object_to_color='plot', stim_status=-1, stim_type=stim_type)
            colors.append(color)
        set_of_lines = plt_coll.LineCollection(segments, colors=colors, linewidth=2, alpha=.7)
        self.ax.add_collection(set_of_lines)
