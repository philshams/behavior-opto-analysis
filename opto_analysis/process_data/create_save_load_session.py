from opto_analysis.process_data.session import Session, get_Session
from opto_analysis.process_data.camera_trigger import get_Camera_trigger
from opto_analysis.process_data.laser import get_Laser
from opto_analysis.process_data.audio import get_Audio
from opto_analysis.process_data.video import get_Video
from pathlib import Path
import os.path
import dill as pickle

def create_session(session_info: list, load: bool=True) -> Session:
    session = get_Session(session_info)
    save_file = os.path.join(session.file_path, "metadata")
    if load and Path(save_file).is_file():
        session = load_session(save_file)
    else:
        session.camera_trigger = get_Camera_trigger(session)
        session.laser = get_Laser(session)
        session.audio = get_Audio(session)
        session.video = get_Video(session)
        save_session(session, overwrite=True)
    return session

def save_session(session: Session, overwrite=True) -> None:
    save_file = os.path.join(session.file_path, "metadata")
    if not Path(save_file).is_file() or overwrite:
        with open(save_file, "wb") as dill_file: pickle.dump(session, dill_file)
    else:
        print('Session file not overwritten for experiment: {}, mouse: {}'.format(session.experiment, session.mouse))

def load_session(save_file: str) -> Session:
    with open(save_file, "rb") as dill_file: session = pickle.load(dill_file)
    return session