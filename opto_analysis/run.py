from settings.settings_process import settings_process as settings_p
from settings.settings_track import settings_track as settings_t
from settings.settings_visualize import settings_visualize as settings_v
from settings.settings_analyze import settings_analyze as settings_a
from opto_analysis.process.process import Process
from opto_analysis.track.track import Track
from opto_analysis.visualize.visualize import Visualize
from opto_analysis.analyze.analyze import Analyze
from opto_analysis.utils.print_settings import print_settings, print_settings_analysis
from opto_analysis.utils.collect_session_IDs import collect_session_IDs, collect_session_IDs_analysis
from databank import databank


def process():
    print("\n------ PROCESSING DATA ------".format(settings_p)); print_settings(settings_p)
    session_IDs = collect_session_IDs(settings_p, databank)
    for session_ID in session_IDs:
        Process(session_ID).create_session(settings_p)

def track():
    print("\n------ TRACKING VIDEOS ------"); print_settings(settings_t)
    session_IDs = collect_session_IDs(settings_t, databank)
    for session_ID in session_IDs:
        session = Process(session_ID).load_session()
        Track(settings_t).run_deeplabcut_tracking(session)
        Track(settings_t).process_tracking_data(session)

def visualize():
    print("\n------ VISUALIZING DATA ------"); print_settings(settings_v)
    session_IDs = collect_session_IDs(settings_v, databank)
    for session_ID in session_IDs:
        session = Process(session_ID).load_session()
        if settings_v.laser_trials:  Visualize(session, settings_v).trials(stim_type = 'laser')
        if settings_v.escape_trials: Visualize(session, settings_v).trials(stim_type = 'audio')

def analyze():
    print("\n------ ANALYZING DATA ------"); print_settings_analysis(settings_a); 
    session_IDs = collect_session_IDs_analysis(settings_a.analysis, databank)
    if settings_a.analysis.plot_escape:  Analyze(session_IDs, settings_a).plot('escape trajectories')
    if settings_a.analysis.plot_laser:   Analyze(session_IDs, settings_a).plot('laser trajectories')
    if settings_a.analysis.plot_targets: Analyze(session_IDs, settings_a).plot('escape targets')