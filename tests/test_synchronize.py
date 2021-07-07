from opto_analysis.process_data.camera_trigger import Camera_trigger
from opto_analysis.process_data.synchronize import verify_all_frames_saved
from opto_analysis.process_data.process_save_load_session import process_session
from sample_data.sample_data_bank import sample_experiments

def test_verify_all_frames_saved():

    session = process_session(sample_experiments[0])
    verify_all_frames_saved(session) # use the assertion contained within this function as the test
    assert True

    session.camera_trigger = Camera_trigger(999, 99, 40)
    try:
        verify_all_frames_saved(session)
        assert False
    except:
        assert True 