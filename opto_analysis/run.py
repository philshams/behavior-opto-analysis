from processing_settings import processing_settings
from analysis_settings import analysis_settings
from opto_analysis.process_data.select_sessions import select_sessions
from opto_analysis.process_data.create_save_load_session import create_session
from opto_analysis.process_data.dlc_tracking import dlc_tracking
from opto_analysis.process_data.synchronize import check_stimulus_sync, verify_all_frames_saved

def process_data():
    print("\n------ PROCESSING DATA ------ \n{}".format(processing_settings))

    selected_sessions_data_entries = select_sessions(processing_settings)
    for data_entry in selected_sessions_data_entries:
        session = create_session(data_entry, create_new=processing_settings.create_new_metadata)
        verify_all_frames_saved(session)

        if processing_settings.examine_laser_trials:
            check_stimulus_sync(session, stimulus_type='laser', rapid=processing_settings.rapid)
        if processing_settings.examine_audio_trials:
            check_stimulus_sync(session, stimulus_type='audio', rapid=processing_settings.rapid)

        if processing_settings.dlc_tracking: 
            dlc_tracking(selected_sessions_data_entries)


def analyze_data():
    print("\n------ ANALYZING DATA ------")
    for key in analysis_settings.__dict__.keys():
        if analysis_settings.__dict__[key]: print(" {} = {}".format(key, analysis_settings.__dict__[key]))
