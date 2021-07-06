from opto_analysis.process_data.session import get_Session

def test_get_Session():
    file_path = ".\\sample_data\\21MAR16_9718_block evs"
    session = get_Session(file_path)
    assert session.date == '21MAR16'
    assert session.mouse == '9718'
    assert session.experiment == 'block evs'
    assert session.DAQ_sampling_rate == 15000
    assert session.fps == 40