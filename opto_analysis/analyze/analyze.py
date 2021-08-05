from opto_analysis.process.process import Process
from opto_analysis.utils.open_tracking_data import open_tracking_data
from opto_analysis.analyze.plot_funcs import *
from opto_analysis.analyze.data_extraction_funcs import *
from opto_analysis.analyze.stats_funcs import permutation_test, print_stat_test_results
from opto_analysis.analyze.analysis_funcs import trial_is_eligible
from opto_analysis.utils.directory import Directory
import matplotlib.pyplot as plt
import numpy as np

class Analyze():
    def __init__(self, session_IDs, settings, analysis_type):
        self.settings = settings
        self.session_IDs = session_IDs
        self.session_count = -1
        self.trial_count = 0
        self.data_x = np.array([])
        self.data_y = np.array([])
        self.data_session_num = np.array([])
        self.trial_colors   = []
        self.trials_to_plot = []
        self.group_nums = np.unique(session_IDs[:, 5])
        self.num_of_groups = np.ptp(self.group_nums)+1 
        self.analysis_type = analysis_type   
        self.title = self.settings.analysis.title
        self.color_by = self.settings.color_by
        if 'traject' in analysis_type and not self.color_by in ['speed', 'speed+RT','time','target', 'session','trial','']:
            self.color_by = 'speed'
        if 'target'  in analysis_type and not self.color_by in ['target', 'session','trial','']:
            self.color_by = 'target'
        if self.settings.leftside_only:  self.title += " (leftside)"
        if self.settings.rightside_only: self.title += " (rightside)"   
        if 'traject' in analysis_type and self.settings.reflect_trajectories: self.title += " (reflect)"
        if analysis_type=='escape trajectories': self.stim_type='audio'
        if analysis_type=='escape targets':      self.stim_type='audio'
        if analysis_type=='laser trajectories':  self.stim_type='laser'

# ----MAIN METHODS------------------------------------------------------
    def trajectories(self):
        self.extract_data()
        self.initialize_trajectory_plot()
        self.plot_trajectories()
        self.save_plot()

    def distribution(self):
        self.extract_data()
        self.do_statistics()
        self.initialize_data_plot()
        self.plot_boxplot()
        self.plot_scatterplot()
        self.save_plot()

# ----DATA EXTRACTION FUNCS----------------------------------------------
    def extract_data(self):
        for session_ID in self.session_IDs:
            self.open_session_data(session_ID) 
            self.get_data_on_each_trial()

    def open_session_data(self, session_ID):
        self.session = Process(session_ID).load_session()
        self.group_num = session_ID[5]
        self.fps = self.session.video.fps
        self.session_count += 1
        self.num_successful_escapes_this_session = 0
        open_tracking_data(self) # generates self.tracking_data

    def get_data_on_each_trial(self):
        for onset_frames, stim_durations in zip(self.session.__dict__[self.stim_type].onset_frames, \
                                                self.session.__dict__[self.stim_type].stimulus_durations):
            if not trial_is_eligible(self, onset_frames): 
                continue
            self.generate_trial_dict(onset_frames, stim_durations)
            self.trial_count+=1

    def generate_trial_dict(self, onset_frames: list, stim_durations: list):
        if self.stim_type=='audio': epochs = ['stimulus']
        if self.stim_type=='laser': epochs = ['stimulus', 'post-laser']
        for epoch in epochs:
            trial_start_idx, trial_end_idx = get_trial_start_and_end(self, onset_frames, stim_durations, epoch)
            trial                          = create_trial_dict(      self, trial_start_idx, trial_end_idx, epoch)
            self.trials_to_plot.append(trial)
        
# ----STATISTICS FUNCS---------------------------------------------------
    def do_statistics(self):
        if not 'trajectories' in self.analysis_type:
            self.compile_all_trials_data()
            self.run_permutation_tests()

    def compile_all_trials_data(self):
        for trial in self.trials_to_plot:
            self.data_x           = np.append(self.data_x, trial['group number'])
            self.data_y           = np.append(self.data_y, trial['escape target score'])
            self.data_session_num = np.append(self.data_session_num, trial['session count'])
            self.trial_colors.         append(get_plot_color(self, trial, plot_type='scatter'))

    def run_permutation_tests(self):
        for group_num in self.group_nums:
            if group_num <= 1: continue
            p = permutation_test(self.data_y,self.data_x,self.data_session_num,group_1=1,group_2=group_num,iterations=1000,two_tailed=self.settings.two_tailed_test)
            print_stat_test_results(p, self.analysis_type, self.settings.two_tailed_test, group_1=1, group_2=group_num,)
       
# ----PLOTTING DATA------------------------------------------------------
    def initialize_data_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(self.num_of_groups*2, 9))
        self.fig.canvas.set_window_title(self.title) 
        self.ax.set_ylim([-.2, 1.2])
        self.x_range = [min(self.group_nums)-.6, max(self.group_nums)+.6]
        self.ax.set_xlim(self.x_range)
        plt.plot(self.x_range, [0,0],     color=(.9,.9,.9), linestyle='--', zorder=-1)
        plt.plot(self.x_range, [1,1],     color=(.9,.9,.9), linestyle='--', zorder=-1)
        plt.plot(self.x_range, [self.settings.edge_vector_threshold,self.settings.edge_vector_threshold], color=(.9,.9,.9), linestyle='--', zorder=-1)
        format_axis(self)

    def plot_scatterplot(self):
        apply_x_jitter(self, offset_x=0, min_distance_y=0.01, jitter_distance_x=0.01 * self.num_of_groups)
        self.ax.scatter(self.jittered_data_x, self.data_y, color=self.trial_colors, linewidth=0, s=35, zorder=99)

    def plot_boxplot(self, width=.25):
        for group_num in self.group_nums:
            group_data_y = self.data_y[self.data_x==group_num]
            quartile_1, median, quartile_3 = np.percentile(group_data_y, [25, 50, 75])
            iqr = quartile_3 - quartile_1
            lower_range = max(min(group_data_y), quartile_1-1.5*iqr)
            upper_range = min(max(group_data_y), quartile_3+1.5*iqr)
            color = (.85,.85,.85)

            whiskers = self.ax.plot([group_num,group_num], [lower_range, upper_range], color=color, linewidth=1)
            boxplot = plt.Rectangle((group_num-width/2, quartile_1), width, iqr, color=color, edgecolor=None, fill=True)
            self.ax.add_artist(boxplot)

            median_line = self.ax.plot([group_num-width/2.15, group_num+width/2.1], [median, median], color=(0,0,0), linewidth=3)

    def save_plot(self):
            # plt.ion()
            plt.show()
            plot_path = Directory(self.settings.save_folder, analysis_type=self.analysis_type, plot=True).\
                        file_name(title=self.title, color_by = self.color_by)
            self.fig.savefig(plot_path, bbox_inches='tight', pad_inches=0) 

# ----PLOTTING TRAJECTORIES-----------------------------------------------
    def initialize_trajectory_plot(self):
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
        format_axis(self)
        self.ax.invert_yaxis()

    def plot_trajectories(self):
        for trial in self.trials_to_plot:
            if self.color_by in ['speed', 'speed+RT','time']: gradient_line(self, trial)
            else:                                             solid_line(self, trial)        