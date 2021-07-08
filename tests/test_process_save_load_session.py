from opto_analysis.process_data.process_save_load_session import process_session, save_session, load_session
from sample_data.sample_data_bank import sample_experiments
from tests.test_camera_trigger import test_camera_trigger
from tests.test_laser import test_laser
from tests.test_audio import test_audio
from tests.test_video import test_video
from tests.test_session import test_session
import dill as pickle
import os

def test_process_save_load_session():

    session = process_session(sample_experiments[0], load_saved=False)
    save_file = os.path.join(session.file_path, "metadata")
    save_session(session, save_file)
    del session
    session = load_session(save_file)

    test_session(session)
    test_camera_trigger(session.camera_trigger)
    test_laser(session.laser)
    test_audio(session.audio)
    test_video(session.video)