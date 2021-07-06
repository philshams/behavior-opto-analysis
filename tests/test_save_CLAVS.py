from opto_analysis.process_data.camera_trigger import get_Camera_trigger
from opto_analysis.process_data.laser import get_Laser
from opto_analysis.process_data.audio import get_Audio
from opto_analysis.process_data.video import get_Video
from opto_analysis.process_data.session import get_Session
from sample_data.sample_data_bank import sample_experiments
from tests.test_camera_trigger import test_camera_trigger
from tests.test_laser import test_laser
from tests.test_audio import test_audio
from tests.test_video import test_video
from tests.test_session import test_session
import dill as pickle
import os

def test_save_CLAVS():
    session = get_Session(sample_experiments[0])
    session.camera_trigger = get_Camera_trigger(session)
    session.laser = get_Laser(session)
    session.audio = get_Audio(session)
    session.video = get_Video(session)

    save_file = os.path.join(session.file_path, "metadata")
    with open(save_file, "wb") as dill_file: pickle.dump(session, dill_file) # save session
    del session # delete session
    with open(save_file, "rb") as dill_file: session = pickle.load(dill_file) # load session

    test_camera_trigger(session.camera_trigger)
    test_laser(session.laser)
    test_audio(session.audio)
    test_video(session.video)
    test_session(session)