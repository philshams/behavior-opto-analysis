from opto_analysis.process_data.session import Session, get_Session
from opto_analysis.process_data.camera_trigger import get_Camera_trigger
from opto_analysis.process_data.laser import get_Laser
from opto_analysis.process_data.audio import get_Audio
from opto_analysis.process_data.video import get_Video
import os
import dill as pickle

# CLAVS ~ Camera, Laser, Audio, Video, Session data

def process_session(session_info: list) -> Session:
    session = get_Session(session_info)
    session.camera_trigger = get_Camera_trigger(session)
    session.laser = get_Laser(session)
    session.audio = get_Audio(session)
    session.video = get_Video(session)
    return session

def save_session(session: Session):
    save_file = os.path.join(session.file_path, "metadata")
    with open(save_file, "wb") as dill_file: pickle.dump(session, dill_file) # save session

def load_session(save_file: str) -> Session:
    with open(save_file, "rb") as dill_file: session = pickle.load(dill_file) # load session
    return session