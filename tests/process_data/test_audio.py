from opto_analysis.process_data.audio import get_Audio
from opto_analysis.process_data.session import get_Session
from opto_analysis.process_data.camera_trigger import get_Camera_trigger
from settings.data_bank import all_data_entries
import numpy as np

def test_audio(audio = None):

    if not audio: # if not provided by another test script
        session = get_Session(all_data_entries[0])
        session.camera_trigger = get_Camera_trigger(session)
        audio = get_Audio(session)

    assert audio.num_samples == 54010500
    assert np.all(audio.onset_frames == np.array([ [54473], [97113], [103703], [113945]]))
    assert np.all(audio.stimulus_durations == np.array([[4.5], [4.5] , [4.5], [3.] ]))
