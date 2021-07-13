from opto_analysis.process.video import get_Video
from settings.data_bank import all_data_entries
from opto_analysis.process.session import get_Session
import cv2

def test_video(video = None):

    if not video: # if not provided by another test script
        session = get_Session(all_data_entries[0])
        video = get_Video(session)

    assert video.num_frames == 143956
    assert video.fps == 40
    assert video.height == 1024
    assert video.width == 1024

    video_object = cv2.VideoCapture(video.video_file)
    video_object.set(cv2.CAP_PROP_POS_FRAMES, 0)
    successful_read, _ = video_object.read()
    assert successful_read
    