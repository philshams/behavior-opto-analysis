from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Session:
    mouse: str
    date: str
    experiment: str
    DAQ_sampling_rate: int=15000
    fps: int=40


def get_Session(file_path: str) -> Session:

    session_folder_name = os.path.basename(file_path)
    date = session_folder_name[:7]
    mouse = session_folder_name[8:12]
    experiment = session_folder_name[13:]

    session = Session(mouse, date, experiment)
    print(session)
    return session
