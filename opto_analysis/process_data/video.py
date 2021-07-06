from opto_analysis.process_data.session import Session
import os
from dataclasses import dataclass
from glob import glob
import cv2

@dataclass(frozen=True)
class Video:
    num_frames: int
    video_file: str

def get_Video(session: Session) -> Video:
    video_file = glob(os.path.join(session.file_path, "cam*"))[-1] # take the last file if there are multiple
    video_object = cv2.VideoCapture(video_file)
    num_frames = video_object.get(cv2.CAP_PROP_FRAME_COUNT)
    video = Video(num_frames, video_file)
    return video