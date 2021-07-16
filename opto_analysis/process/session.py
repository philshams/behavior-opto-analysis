from dataclasses import dataclass
from settings.data_bank import data_path
import os

@dataclass(frozen=False)
class Session:
    name: str
    number: int
    mouse: str
    date: str
    experiment: str
    previous_sessions: int
    file_path: str
    metadata_file: str
    daq_sampling_rate: int=15000
    camera_trigger: object=None
    laser: object=None
    audio: object=None
    video: object=None

def get_Session(session_info: list) -> Session:
    local_session_number = session_info[0]
    global_session_number = session_info[1]
    experiment = session_info[2]
    num_previous_sessions = session_info[3]
    file_path = os.path.join(data_path, session_info[4])
    metadata_file = os.path.join(file_path, "metadata")
    session_folder_name = os.path.basename(file_path)
    date = session_folder_name[:7]
    mouse = session_folder_name[8:12]
    name = experiment + ' ' + str(local_session_number)   
    session = Session(name, global_session_number, mouse, date, experiment, num_previous_sessions, file_path, metadata_file)
    return session
