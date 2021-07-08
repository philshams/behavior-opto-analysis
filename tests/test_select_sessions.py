from opto_analysis.process_data.select_sessions import select_sessions_to_analyze
from opto_analysis.program import Program
import numpy as np

def test_select_sessions_to_analyze():
    program = Program(process_data=True, analyze_particular_sessions=True, sessions_to_analyze=[1])
    selected_sessions = select_sessions_to_analyze(program)
    assert selected_sessions.shape == (1, 5)
    assert np.all(selected_sessions[:,0]==1)

    program = Program(process_data=True, analyze_particular_experiments=True, experiments_to_analyze=['fake experiment','block edge vectors'])
    selected_sessions = select_sessions_to_analyze(program)
    assert selected_sessions.shape == (2, 5)
    assert np.all(selected_sessions[:,2]=="block edge vectors")

    program = Program(process_data=True, analyze_particular_sessions=True, sessions_to_analyze=[0,-3,999999], analyze_particular_experiments=True, experiments_to_analyze=['fake experiment','block edge vectors'])
    selected_sessions = select_sessions_to_analyze(program)
    assert selected_sessions.shape == (1, 5)
    assert np.all(selected_sessions[:,2]=="block edge vectors")
    assert np.all(selected_sessions[:,0]==0)

    program = Program(process_data=True, analyze_particular_naivete=True, num_previous_sessions_to_analyze=[2])
    selected_sessions = select_sessions_to_analyze(program)
    assert selected_sessions.shape == (0, 5)

    program = Program(process_data=True, analyze_particular_experiments=True, experiments_to_analyze='block edge vectors')
    try:
        selected_sessions = select_sessions_to_analyze(program)
        assert False
    except:
        assert True

