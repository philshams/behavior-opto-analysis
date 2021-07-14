from opto_analysis.process.session import Session, get_Session
from opto_analysis.process.camera_trigger import get_Camera_trigger
from opto_analysis.process.laser import get_Laser
from opto_analysis.process.audio import get_Audio
from opto_analysis.process.video import get_Video
from opto_analysis.process.synchronize import verify_all_frames_saved, verify_aligned_data_streams
from settings.processing_settings import processing_settings
from pathlib import Path
import os.path
import numpy as np
import dill as pickle

def create_session(session_info: list, create_new: bool=False) -> Session:
    session = get_Session(session_info)
    save_file = os.path.join(session.file_path, "metadata")

    if Path(save_file).is_file and isinstance(load_session(save_file).video.registration_transform, np.ndarray) and not processing_settings.skip_registration:
        loaded_registration_transform = load_session(save_file).video.registration_transform
    else: loaded_registration_transform = None

    if create_new or not Path(save_file).is_file():
        session.camera_trigger = get_Camera_trigger(session)
        session.laser = get_Laser(session)
        session.audio = get_Audio(session)
        session.video = get_Video(session, loaded_registration_transform)
        print_session_details(session)
        verify_all_frames_saved(session)
        verify_aligned_data_streams(session)
        save_session(session, overwrite=True)
    else:
        session = load_session(save_file)
    return session

def save_session(session: Session, overwrite=True) -> None:
    save_file = os.path.join(session.file_path, "metadata")
    if not Path(save_file).is_file() or overwrite:
        with open(save_file, "wb") as dill_file: pickle.dump(session, dill_file)

def load_session(save_file: str) -> Session:
    with open(save_file, "rb") as dill_file: session = pickle.load(dill_file)
    return session

def print_session_details(session: Session) -> None:
    for key in session.__dict__.keys():
        if key in ['name','number','mouse','date','experiment','previous_sessions']:
            print(" {}: {}".format(key, session.__dict__[key]))
        elif key in ['camera_trigger', 'laser','audio','video']:
            if key == 'camera_trigger': print("")
            print(" {} metadata saved".format(key))
    print(" registration transform: {}".format(isinstance(session.video.registration_transform, np.ndarray)))
    print(" -----------------")