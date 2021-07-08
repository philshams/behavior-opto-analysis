from opto_analysis.process_data.session import Session, get_Session
from opto_analysis.process_data.camera_trigger import get_Camera_trigger
from opto_analysis.process_data.laser import get_Laser
from opto_analysis.process_data.audio import get_Audio
from opto_analysis.process_data.video import get_Video
import os
import dill as pickle

# TODO: automatically open saved session if there is one; add overwrite option

# TODO: DLC tracking (new file)

def process_session(session_info: list, load_saved: bool=True) -> Session:
    session = get_Session(session_info)
    save_file = os.path.join(session.file_path, "metadata")
    if is_file(save_file) and load_saved:
        session = load_session(save_file)
    else:
        session.camera_trigger = get_Camera_trigger(session)
        session.laser = get_Laser(session)
        session.audio = get_Audio(session)
        session.video = get_Video(session)
    return session

def save_session(session: Session, save_file: str, overwrite=True) -> None:
    if not is_file(save_file) or overwrite:
        with open(save_file, "wb") as dill_file: pickle.dump(session, dill_file)
    else:
        print('Session file not overwritten for experiment: {}, mouse: {}'.format(session.experiment, session.mouse))

def load_session(save_file: str) -> Session:
    with open(save_file, "rb") as dill_file: session = pickle.load(dill_file)
    return session