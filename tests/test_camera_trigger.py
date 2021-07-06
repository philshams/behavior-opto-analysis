from opto_analysis.process_data.camera_trigger import get_Camera_trigger
from opto_analysis.process_data.session import get_Session
import numpy as np


def test_camera_trigger():
    file_path = ".\\sample_data\\21MAR16_9718_block evs"
    session = get_Session(file_path)
    
    camera_trigger = get_Camera_trigger(file_path, session)

    assert camera_trigger.num_samples == 54010500
    assert camera_trigger.num_frames == 143956
    assert camera_trigger.fps == 40

    