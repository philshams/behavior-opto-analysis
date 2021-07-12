from opto_analysis.process.session import Session
from opto_analysis.process.registration import get_registration_transform
from settings.processing_settings import processing_settings

import os
from dataclasses import dataclass
from glob import glob
import cv2

@dataclass(frozen=True)
class Video:
    num_frames: int
    video_file: str
    fps: int
    registration_transform: object
    x_offset: int=0 # if the video frame is cropped, how far from the top left edge is it
    y_offset: int=0 # (this is for the fisheye correction step)
    # TODO: find out if nonzero x and y offset are needed

def get_Video(session: Session) -> Video:
    video_file = glob(os.path.join(session.file_path, "cam*avi"))[-1] # take the last file if there are multiple
    video_object = cv2.VideoCapture(video_file)
    num_frames = video_object.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video_object.get(cv2.CAP_PROP_FPS)
    registration_transform = get_registration_transform(session, video_object)
    video = Video(num_frames, video_file, fps, registration_transform)
    return video

