from opto_analysis.process.camera_trigger import Camera_trigger
from opto_analysis.process.synchronize import verify_all_frames_saved, verify_aligned_data_streams
from opto_analysis.process.create_save_load_session import create_session
from settings.data_bank import all_data_entries
import numpy as np

def test_verify_synchronized():

    session = create_session(all_data_entries[0])
    verify_all_frames_saved(session) # use the assertion contained within this function as the test
    verify_aligned_data_streams(session) # use the assertion contained within this function as the test
    assert True

    session.camera_trigger = Camera_trigger(999, 99, np.array([0,1,2]), 40)
    try:
        verify_all_frames_saved(session)
        assert False
    except:
        assert True

    try:
        verify_aligned_data_streams(session)
        assert False
    except:
        assert True
