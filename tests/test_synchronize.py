from opto_analysis.process_data.camera_trigger import Camera_trigger
from opto_analysis.process_data.synchronize import check_stimulus_sync, verify_all_frames_saved
from opto_analysis.process_data.process_save_load_session import load_session, create_session
from data_bank import all_experiments

def test_verify_all_frames_saved():

    session = create_session(all_experiments[0], load_saved=True)
    verify_all_frames_saved(session) # use the assertion contained within this function as the test
    assert True

    session.camera_trigger = Camera_trigger(999, 99, 40)
    try:
        verify_all_frames_saved(session)
        assert False
    except:
        assert True 

def test_check_laser_sync():
    session = create_session(all_experiments[0])
    check_stimulus_sync(session, stimulus_type='laser', rapid=True)

def test_check_audio_sync():
    session = create_session(all_experiments[0])
    check_stimulus_sync(session, stimulus_type='audio', rapid=True)