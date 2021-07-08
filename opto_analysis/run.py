from analysis_program import settings_name, settings
from opto_analysis.process_data.select_sessions import select_sessions_to_analyze
from opto_analysis.process_data.create_save_load_session import create_session
from opto_analysis.dlc_tracking.dlc_tracking import dlc_tracking
from opto_analysis.process_data.synchronize import check_stimulus_sync, verify_all_frames_saved
from opto_analysis.analysis.analysis import analysis
from opto_analysis.plotting.plotting import plotting

def run():
    print("\n------ {} ------ \n{}".format(settings_name, settings))

    selected_sessions_data_entries = select_sessions_to_analyze(settings)
    for data_entry in selected_sessions_data_entries:
        session = create_session(data_entry, load=settings.load_metadata)

        if settings.verify_data_sync:
            verify_all_frames_saved(session)
            check_stimulus_sync(session, stimulus_type='laser', rapid=True)
            check_stimulus_sync(session, stimulus_type='audio', rapid=False)

        if settings.dlc_tracking: 
            dlc_tracking(selected_sessions_data_entries)

    if settings.plotting: 
        plotting()

if __name__=="__main__":
    run()
