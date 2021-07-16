from opto_analysis.process.session import Session
from opto_analysis.track.register import Register
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
    height: int
    width: int
    fisheye_correction_file: str
    rendering_size_pixels: int
    x_offset: int=128 # if the video frame is cropped, how far from the top left edge is it
    y_offset: int=0   # (this is for the fisheye correction step)

def get_Video(session: Session, registration_transform: object=None) -> Video:
    video_file = glob(os.path.join(session.file_path, "cam*avi"))[-1] # take the last file if there are multiple
    video_object = cv2.VideoCapture(video_file)
    num_frames = video_object.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video_object.get(cv2.CAP_PROP_FPS)
    height = int(video_object.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(video_object.get(cv2.CAP_PROP_FRAME_WIDTH))
    fisheye_correction_file = processing_settings.fisheye_correction_file
    rendering_size_pixels = processing_settings.size

    video = Video(num_frames, video_file, fps, None, height, width, fisheye_correction_file, rendering_size_pixels)
    if processing_settings.skip_registration: return video

    if processing_settings.create_new_registration or (isinstance(registration_transform, type(None)) and not processing_settings.skip_registration):
        registration_transform = Register(session, video, video_object).transform
        
    video = Video(num_frames, video_file, fps, registration_transform, height, width, fisheye_correction_file, rendering_size_pixels)
    return video