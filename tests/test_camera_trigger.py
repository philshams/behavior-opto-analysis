from opto_analysis.process_data.camera_trigger import get_Camera_trigger
from opto_analysis.process_data.session import get_Session
from sample_data.sample_data_bank import sample_experiments
import numpy as np


def test_camera_trigger(camera_trigger = None):

    if not camera_trigger: # if not provided by another test script
        session = get_Session(sample_experiments[0])
        camera_trigger = get_Camera_trigger(session)

    assert camera_trigger.num_samples == 54010500
    assert camera_trigger.num_frames == 143956
    assert camera_trigger.fps == 40

    