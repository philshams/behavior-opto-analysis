from opto_analysis.process.session import Session
from settings.processing_settings import processing_settings
import cv2

def get_registration_transform(session: Session, video_object: object) -> object:
    if processing_settings.skip_registration:
        return None

