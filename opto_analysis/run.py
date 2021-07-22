from settings.settings_process import settings_process
from settings.settings_track import settings_track
from settings.settings_analyze import settings_analyze
from settings.settings_visualize import settings_visualize
from opto_analysis.process.process import Process
from opto_analysis.track.track import Track
from opto_analysis.visualize.visualize import Visualize
from opto_analysis.analyze.analyze import Analyze
from opto_analysis.utils.print_settings import print_settings
from opto_analysis.utils.collect_session_IDs import collect_session_IDs, collect_session_IDs_analysis
from databank import databank


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
    selected_session_IDs = collect_session_IDs_analysis(settings_analyze, databank)
    if settings_analyze.plot_escapes:         Analyze(selected_session_IDs, settings_analyze).escapes()
    if settings_analyze.plot_laser_responses: Analyze(selected_session_IDs, settings_analyze).laser_responses()