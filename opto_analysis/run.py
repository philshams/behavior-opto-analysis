from settings.settings_process import settings_process
from settings.settings_track import settings_track
from settings.settings_analyze import settings_analyze
from settings.settings_visualize import settings_visualize
from opto_analysis.process.process import Process
from opto_analysis.track.track import Track
from opto_analysis.visualize.visualize import Visualize
from databank import databank
import os
import numpy as np


def process():
    print("\n------ PROCESSING DATA ------".format(settings_process)); print_settings(settings_process)
    selected_session_IDs = collect_session_IDs(settings_process, databank)
    for session_ID in selected_session_IDs:
        Process(session_ID).create_session(settings_process)

def track():
    print("\n------ TRACKING VIDEOS ------"); print_settings(settings_track)
    selected_session_IDs = collect_session_IDs(settings_track, databank)
    for session_ID in selected_session_IDs:
        session = Process(session_ID).load_session()
        Track(settings_track).run_deeplabcut_tracking(session)
        Track(settings_track).process_tracking_data(session)

def visualize():
    print("\n------ VISUALIZING DATA ------"); print_settings(settings_visualize)
    selected_session_IDs = collect_session_IDs(settings_visualize, databank)
    for session_ID in selected_session_IDs:
        session = Process(session_ID).load_session()
        if settings_visualize.laser_trials:  Visualize(session, settings_visualize).trials(stimulus_type = 'laser')
        if settings_visualize.escape_trials: Visualize(session, settings_visualize).trials(stimulus_type = 'audio')

def analyze():
    print("\n------ ANALYZING DATA ------"); print_settings(settings_analyze)
    selected_session_IDs = collect_session_IDs(settings_analyze, databank)
    for session_ID in selected_session_IDs:
        session = Process(session_ID).load_session()

# ----------------------------------------------------------------------------------------------------------

def print_settings(settings: object):
    for key in settings.__dict__.keys():
        if settings.__dict__[key] and not key in ['by_experiment', 'experiments', 'by_session', 'sessions', 'by_prev_session', 'prev_session']:
            print(" {}: {}".format(key, settings.__dict__[key]))
    if settings.by_experiment: print(" - experiments: {}".format(settings.experiments))
    if settings.by_session: print(" - sessions: {}".format(settings.sessions))
    if settings.by_prev_session: print(" - # of prev sessions: {}".format(settings.prev_sessions))
    print('\n-----------------')

def collect_session_IDs(settings: object, databank: list) -> object:
    session_IDs = np.array(databank['session IDs'], dtype='object')

    if settings.by_experiment:
        assert isinstance(settings.experiments, list), "Experiment(s) must be listed in list format"
        experiments_idx = np.sum([experiment==session_IDs[:,2] for experiment in settings.experiments],0).astype(bool)
        session_IDs = session_IDs[experiments_idx]

    if settings.by_prev_session:
        assert isinstance(settings.prev_session, list), "Number(s) of previous sessions must be listed in list format"
        naivete_idx = np.sum([num_prev_sessions==session_IDs[:,3] for num_prev_sessions in settings.prev_session],0).astype(bool)
        session_IDs = session_IDs[naivete_idx]

    if settings.by_session:
        assert isinstance(settings.sessions, list), "Session number(s) must be listed in list format"
        session_idx = np.sum([session_num==session_IDs[:,0] for session_num in settings.sessions],0).astype(bool)
        session_IDs = session_IDs[session_idx]

    for entry in session_IDs: # add in the full path to the raw data
        entry[4] = os.path.join(databank['path'], entry[4])

    return session_IDs