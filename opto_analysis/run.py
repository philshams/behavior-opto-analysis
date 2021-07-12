from settings.processing_settings import processing_settings
from settings.tracking_settings import tracking_settings
from settings.analysis_settings import analysis_settings
from settings.visualization_settings import visualization_settings
from opto_analysis.process.select_sessions import select_sessions
from opto_analysis.process.create_save_load_session import create_session
from opto_analysis.dlc_tracking import dlc_tracking
from opto_analysis.visualize.trials import visualize_trials
from opto_analysis.visualize.exploration import visualize_exploration

def process_data():
    print("\n------ PROCESSING DATA ------".format(processing_settings))
    print_settings(processing_settings)
    selected_sessions_data_entries = select_sessions(processing_settings)
    for data_entry in selected_sessions_data_entries:
        create_session(data_entry, create_new=True)

def track_data():
    print("\n------ TRACKING MICE ------")
    print_settings(tracking_settings)
    selected_sessions_data_entries = select_sessions(tracking_settings)
    for data_entry in selected_sessions_data_entries:
        session = create_session(data_entry, create_new=False)
        dlc_tracking(session, tracking_settings)

def visualize_data():
    print("\n------ VISUALIZING THE DATA ------")
    print_settings(visualization_settings)
    selected_sessions_data_entries = select_sessions(visualization_settings)
    for data_entry in selected_sessions_data_entries:
        session = create_session(data_entry, create_new=False)
        if visualization_settings.visualize_laser_trials: 
            visualize_trials(session, visualization_settings, stimulus_type = 'laser', rapid=visualization_settings.rapid, rendering=visualization_settings.generate_rendering, seconds_before=3, seconds_after=6)
        if visualization_settings.visualize_escape_trials: 
            visualize_trials(session, visualization_settings, stimulus_type = 'audio', rapid=visualization_settings.rapid, rendering=visualization_settings.generate_rendering, seconds_before=3, seconds_after=2)
        if visualization_settings.visualize_exploration: 
            visualize_exploration(session)

def analyze_data():
    print("\n------ ANALYZING DATA ------")
    print_settings(analysis_settings)
    selected_sessions_data_entries = select_sessions(analysis_settings)
    for data_entry in selected_sessions_data_entries:
        session = create_session(data_entry, create_new=False)

def print_settings(settings: object):

    for key in settings.__dict__.keys():
        if settings.__dict__[key] and not key in ['by_experiment', 'experiments', 'by_session', 'sessions', 'by_prev_session', 'prev_session']:
            print(" {}: {}".format(key, settings.__dict__[key]))

    if settings.by_experiment: print(" - experiments: {}".format(settings.experiments))
    if settings.by_session: print(" - sessions: {}".format(settings.sessions))
    if settings.by_prev_session: print(" - # of prev sessions: {}".format(settings.prev_sessions))

