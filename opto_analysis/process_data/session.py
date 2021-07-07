from dataclasses import dataclass
import os


@dataclass(frozen=False)
class Session:
    mouse: str
    date: str
    experiment: str
    previous_sessions: int
    file_path: str
    daq_sampling_rate: int=15000
    fps: int=40
    camera_trigger: object=None
    laser: object=None
    audio: object=None
    video: object=None


    
def get_Session(session_info: list) -> Session:

    file_path = session_info[2]
    session_folder_name = os.path.basename(file_path)
    date = session_folder_name[:7]
    mouse = session_folder_name[8:12]
    experiment = session_info[0]
    previous_sessions = session_info[1]

    session = Session(mouse, date, experiment, previous_sessions, file_path)
    print(session)
    return session
