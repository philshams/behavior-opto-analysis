from opto_analysis.process_data.session import get_Session
from data_bank import all_data_entries

def test_session(session=None):
    if not session:
        session = get_Session(all_data_entries[0])
    assert session.date == '21MAR16'
    assert session.mouse == '9718'
    assert session.experiment == 'block edge vectors'
    assert session.daq_sampling_rate == 15000
    assert session.fps == 40
    assert session.previous_sessions == 0