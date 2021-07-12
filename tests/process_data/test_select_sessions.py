from opto_analysis.process.select_sessions import select_sessions
from opto_analysis.settings_objects import Processing_settings
import numpy as np

def test_select_sessions_to_analyze():
    program = Processing_settings(by_session=True, sessions=[1])
    selected_sessions = select_sessions(program)
    assert selected_sessions.shape == (1, 5)
    assert np.all(selected_sessions[:,0]==1)

    program = Processing_settings(by_experiment=True, experiments=['fake experiment','block edge vectors'])
    selected_sessions = select_sessions(program)
    assert selected_sessions.shape == (8, 5)
    assert np.all(selected_sessions[:,2]=="block edge vectors")

    program = Processing_settings(by_session=True, sessions=[0,-3,999999], by_experiment=True, experiments=['fake experiment','block edge vectors'])
    selected_sessions = select_sessions(program)
    assert selected_sessions.shape == (1, 5)
    assert np.all(selected_sessions[:,2]=="block edge vectors")
    assert np.all(selected_sessions[:,0]==0)

    program = Processing_settings(by_prev_session=True, prev_session=[np.nan])
    selected_sessions = select_sessions(program)
    assert selected_sessions.shape == (0, 5)

    program = Processing_settings(by_experiment=True, experiments='block edge vectors')
    try:
        selected_sessions = select_sessions(program)
        assert False
    except:
        assert True

