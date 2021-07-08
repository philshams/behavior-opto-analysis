from opto_analysis.process_data.create_save_load_session import create_session
from data_bank import all_sessions
from tests.test_camera_trigger import test_camera_trigger
from tests.test_laser import test_laser
from tests.test_audio import test_audio
from tests.test_video import test_video
from tests.test_session import test_session


def test_create_save_load_session():

    session = create_session(all_sessions[0], load=False)
    del session
    session = create_session(all_sessions[0], load=True)

    test_session(session)
    test_camera_trigger(session.camera_trigger, session)
    test_laser(session.laser)
    test_audio(session.audio)
    test_video(session.video)