from opto_analysis.process_data.laser import get_Laser
from opto_analysis.process_data.session import get_Session
from sample_data.sample_data_bank import sample_experiments
import numpy as np


def test_Laser():
    session = get_Session(sample_experiments[0])
    onset_frames = np.array([np.array([2696, 2832]), np.array([5000, 5124, 5252])], dtype=object)
    stimulus_durations = np.array([np.array([2., 2.]), np.array([2., 2., 2.])], dtype=object)

    laser = get_Laser(session)

    assert laser.num_samples == 54004500

    assert np.all([np.all(l) for l in [x == y for x, y in zip(
        laser.onset_frames, onset_frames)]])

    assert np.all([np.all(l) for l in [x == y for x, y in zip(
        laser.stimulus_durations, stimulus_durations)]])

    assert np.all(laser.frequency == np.array([20., 20.]))
