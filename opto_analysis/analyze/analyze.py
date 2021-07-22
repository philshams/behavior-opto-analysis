from opto_analysis.process.process import Process
from opto_analysis.utils.open_tracking_data import open_tracking_data
import matplotlib.pyplot as plt

class Analyze():
    def __init__(self, selected_session_IDs, settings):
        self.settings = settings
        self.selected_session_IDs = selected_session_IDs[0]
        self.selected_session_IDs_group_A = selected_session_IDs[1]
        self.selected_session_IDs_group_B = selected_session_IDs[2]

    def escapes(self):
        self.plot_arena()
        self.plot_escapes(group='A')
        self.plot_escapes(group='B')
        self.save_plot()

    def laser_responses(self):
        self.plot_arena()


# ---------------------------------------------------------


    def plot_escapes(self, group='A'):
        self.select_which_set_of_sessions_to_plot(group='A')
        for session_ID in self.current_selected_session_IDs:
            self.session = Process(session_ID).load_session()
            open_tracking_data(self)
            for onset_frames in self.session.audio.onset_frames:
                if self.determine_trial_eligibility().ineligible: continue
                self.plot_escape_trial(onset_frames)
            

# ---------------------------------------------------------

    def plot_arena(self):
        plt.figure()
        pass
    
    def plot_escape_trial(self, trial_num):
        pass

    def select_which_sessions_to_plot(self, group: str='A'):
        if not self.settings.compare:
            self.current_selected_session_IDs = self.selected_session_IDs
        elif self.settings.compare and group=='A':
            self.current_selected_session_IDs = self.selected_session_IDs_group_A
        elif self.settings.compare and group == 'B':
            self.current_selected_session_IDs = self.selected_session_IDs_group_B

    def determine_trial_eligibility(self):
        if self.current_num_successful_escapes >= self.settings.max_escapes_per_mouse or \
        not self.current_trial_is_successful_escape():
            self.ineligible = True

