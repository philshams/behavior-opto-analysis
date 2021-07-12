from opto_analysis.process_data.laser import get_Laser
from opto_analysis.process_data.session import get_Session
from opto_analysis.process_data.camera_trigger import get_Camera_trigger
from settings.data_bank import all_data_entries
import numpy as np


def test_laser(laser = None):

    if not laser: # if not provided by another test script
        session = get_Session(all_data_entries[0])
        session.camera_trigger = get_Camera_trigger(session)
        laser = get_Laser(session)

    onset_frames = np.array([np.array([2696, 2832]), np.array([5000, 5124, 5252])], dtype=object)
    stimulus_durations = np.array([np.array([2., 2.]), np.array([2., 2., 2.])], dtype=object)   

    assert laser.num_samples == 54004500
    assert np.all([np.all(l) for l in [x == y for x, y in zip(laser.onset_frames, onset_frames)]])
    assert np.all([np.all(l) for l in [x == y for x, y in zip(laser.stimulus_durations, stimulus_durations)]])
    assert np.all(laser.frequency == np.array([20., 20.]))
