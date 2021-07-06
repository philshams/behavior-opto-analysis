from opto_analysis.process_data.audio import get_Audio
from opto_analysis.process_data.session import get_Session
import numpy as np


def test_audio():
    file_path = ".\\sample_data\\21MAR16_9718_block evs"
    session = get_Session(file_path)
    audio = get_Audio(file_path, session)

    assert audio.num_samples == 54010500
    assert np.all(audio.onset_frames == np.array([ 54477,  97118, 103708, 113949]))
    assert np.all(audio.stimulus_durations == np.array([1.5, 3. , 1.5, 3. ]))
    assert np.all(audio.amplitude == np.array([87., 81., 87., 81.]))
