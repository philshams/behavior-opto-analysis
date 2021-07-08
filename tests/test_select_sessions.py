from opto_analysis.process_data.select_sessions import select_sessions_to_analyze
from opto_analysis.program import Analysis_settings
import numpy as np

def test_select_sessions_to_analyze():
    program = Analysis_settings(process_data=True, by_session=True, sessions=[1])
    selected_sessions = select_sessions_to_analyze(program)
    assert selected_sessions.shape == (1, 5)
    assert np.all(selected_sessions[:,0]==1)

    program = Analysis_settings(process_data=True, by_experiment=True, experiments=['fake experiment','block edge vectors'])
    selected_sessions = select_sessions_to_analyze(program)
    assert selected_sessions.shape == (2, 5)
    assert np.all(selected_sessions[:,2]=="block edge vectors")

    program = Analysis_settings(process_data=True, by_session=True, sessions=[0,-3,999999], by_experiment=True, experiments=['fake experiment','block edge vectors'])
    selected_sessions = select_sessions_to_analyze(program)
    assert selected_sessions.shape == (1, 5)
    assert np.all(selected_sessions[:,2]=="block edge vectors")
    assert np.all(selected_sessions[:,0]==0)

    program = Analysis_settings(process_data=True, by_prev_session=True, prev_session=[2])
    selected_sessions = select_sessions_to_analyze(program)
    assert selected_sessions.shape == (0, 5)

    program = Analysis_settings(process_data=True, by_experiment=True, experiments='block edge vectors')
    try:
        selected_sessions = select_sessions_to_analyze(program)
        assert False
    except:
        assert True

