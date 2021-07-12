from opto_analysis.process.camera_trigger import Camera_trigger, get_Camera_trigger
from opto_analysis.process.session import get_Session, Session
from settings.data_bank import all_data_entries



def test_camera_trigger(camera_trigger: Camera_trigger=None, session: Session=None):   
    if not camera_trigger: # if not provided by another test script
        session = get_Session(all_data_entries[0])
        camera_trigger = get_Camera_trigger(session)

    assert camera_trigger.num_samples == 54010500
    assert camera_trigger.num_frames == 143956
    assert camera_trigger.fps == 40

    