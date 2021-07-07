from opto_analysis.process_data.audio import get_Audio
from opto_analysis.process_data.session import get_Session
from sample_data.sample_data_bank import sample_experiments
import numpy as np

def test_audio(audio = None):

    if not audio: # if not provided by another test script
        session = get_Session(sample_experiments[0])
        audio = get_Audio(session)

    assert audio.num_samples == 54010500
    assert np.all(audio.onset_frames == np.array([ 54477, 97117, 103707, 113949]))
    assert np.all(audio.stimulus_durations == np.array([1.5, 3. , 1.5, 3. ]))
    assert np.all(audio.amplitude == np.array([87., 81., 87., 81.]))
