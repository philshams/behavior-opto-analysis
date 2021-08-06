from opto_analysis.process.session import Session
from opto_analysis.track.register import Register
from dataclasses import dataclass
from glob import glob
import numpy as np
import cv2
import os

@dataclass(frozen=True)
class Video:
    num_frames: int
    video_file: str
    fps: int
    registration_transform: object
    height: int
    width: int
    fisheye_correction_file: str
    rendering_size_pixels: int #TODO: make this a tuple (width, height)
    pixels_per_cm: int
    tracking_data_file: str
    #! replace these values with your own parameters
    shelter_location: tuple=(512, 921)
    x_offset: int=128 # if the video frame is cropped, how far from the top left edge is it
    y_offset: int=0   # (this is for the fisheye correction step)

def get_Video(session: Session, settings: object, registration_transform: object=None) -> Video:
    video_file = glob(os.path.join(session.file_path, "cam*avi"))[-1] # take the last file if there are multiple
    video_object = cv2.VideoCapture(video_file)
    num_frames = int(video_object.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(video_object.get(cv2.CAP_PROP_FPS))
    height = int(video_object.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(video_object.get(cv2.CAP_PROP_FRAME_WIDTH))
    fisheye_correction_file = settings.fisheye_correction_file
    rendering_size_pixels = settings.size
    pixels_per_cm = settings.pixels_per_cm
    tracking_data_file = os.path.join(session.file_path, "tracking")

    video = Video(num_frames, video_file, fps, registration_transform, height, width, fisheye_correction_file, rendering_size_pixels, pixels_per_cm, tracking_data_file)
    if settings.skip_registration or (isinstance(registration_transform, np.ndarray) and not settings.create_new_registration): 
        return video

    registration_transform = Register(session, video, video_object).transform
    video = Video(num_frames, video_file, fps, registration_transform, height, width, fisheye_correction_file, rendering_size_pixels, pixels_per_cm, tracking_data_file)
    return video