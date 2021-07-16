from settings.processing_settings import processing_settings
from settings.tracking_settings import tracking_settings
from settings.analysis_settings import analysis_settings
from settings.visualization_settings import visualization_settings
from opto_analysis.process.process import Process
from opto_analysis.track.dlc_tracking import dlc_tracking
from opto_analysis.visualize.visualize import Visualize
from settings.data_bank import all_data_entries
import numpy as np


def process_data():
    print("\n------ PROCESSING DATA ------".format(processing_settings))
    print_settings(processing_settings)
    selected_sessions_data_entries = select_sessions(processing_settings)
    for data_entry in selected_sessions_data_entries:
        Process(data_entry).create_session()

def track_data():
    print("\n------ TRACKING MICE ------")
    print_settings(tracking_settings)
    selected_sessions_data_entries = select_sessions(tracking_settings)
    for data_entry in selected_sessions_data_entries:
        session = Process(data_entry).load_session()
        dlc_tracking(session, tracking_settings)

def visualize_data():
    print("\n------ VISUALIZING THE DATA ------")
    print_settings(visualization_settings)
    selected_sessions_data_entries = select_sessions(visualization_settings)
    for data_entry in selected_sessions_data_entries:
        session = Process(data_entry).load_session()
        if visualization_settings.visualize_laser_trials:
            Visualize(session).trials(stimulus_type = 'laser', seconds_before=3, seconds_after=6)
        if visualization_settings.visualize_escape_trials: 
            Visualize(session).trials(stimulus_type = 'audio', seconds_before=3, seconds_after=2)

def analyze_data():
    print("\n------ ANALYZING DATA ------")
    print_settings(analysis_settings)
    selected_sessions_data_entries = select_sessions(analysis_settings)
    for data_entry in selected_sessions_data_entries:
        session = Process(data_entry).load_session()

# ----------------------------------------------------------------------------------------------------------

def print_settings(settings: object):
    for key in settings.__dict__.keys():
        if settings.__dict__[key] and not key in ['by_experiment', 'experiments', 'by_session', 'sessions', 'by_prev_session', 'prev_session']:
            print(" {}: {}".format(key, settings.__dict__[key]))
    if settings.by_experiment: print(" - experiments: {}".format(settings.experiments))
    if settings.by_session: print(" - sessions: {}".format(settings.sessions))
    if settings.by_prev_session: print(" - # of prev sessions: {}".format(settings.prev_sessions))
    print('\n-----------------')

def select_sessions(processing_settings: object) -> object:
    selected_sessions = np.array(all_data_entries, dtype='object')

    if processing_settings.by_experiment:
        assert isinstance(processing_settings.experiments, list), "Experiment(s) must be listed in list format"
        experiments_idx = np.sum([experiment==selected_sessions[:,2] for experiment in processing_settings.experiments],0).astype(bool)
        selected_sessions = selected_sessions[experiments_idx]

    if processing_settings.by_prev_session:
        assert isinstance(processing_settings.prev_session, list), "Number(s) of previous sessions must be listed in list format"
        naivete_idx = np.sum([num_prev_sessions==selected_sessions[:,3] for num_prev_sessions in processing_settings.prev_session],0).astype(bool)
        selected_sessions = selected_sessions[naivete_idx]

    if processing_settings.by_session:
        assert isinstance(processing_settings.sessions, list), "Session number(s) must be listed in list format"
        session_idx = np.sum([session_num==selected_sessions[:,0] for session_num in processing_settings.sessions],0).astype(bool)
        selected_sessions = selected_sessions[session_idx]

    return selected_sessions