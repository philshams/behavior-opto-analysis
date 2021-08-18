from dataclasses import dataclass
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
    spontaneous: object = None

def get_Session(session_ID: list) -> Session:
    global_session_number = session_ID[0]
    local_session_number = session_ID[1]
    experiment = session_ID[2]
    num_previous_sessions = session_ID[3]
    file_path = session_ID[4]
    metadata_file = os.path.join(file_path, "metadata")
    session_folder_name = os.path.basename(file_path)
    date = session_folder_name[:7]
    mouse = session_folder_name[8:12]
    name = experiment + ' ' + str(local_session_number)   
    session = Session(name, global_session_number, mouse, date, experiment, num_previous_sessions, file_path, metadata_file)
    return session
