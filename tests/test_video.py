from opto_analysis.process_data.video import get_Video
from sample_data.sample_data_bank import sample_experiments
from opto_analysis.process_data.session import get_Session
import cv2

def test_video(video = None):

    if not video: # if not provided by another test script
        session = get_Session(sample_experiments[0])
        video = get_Video(session)

    assert video.num_frames == 143956

    video_object = cv2.VideoCapture(video.video_file)
    video_object.set(cv2.CAP_PROP_POS_FRAMES, 0)
    successful_read, _ = video_object.read()
    assert successful_read
    