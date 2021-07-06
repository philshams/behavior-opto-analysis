from opto_analysis.process_data.video import get_Video
import cv2

def test_audio():
    file_path = ".\\sample_data\\21MAR16_9718_block evs"
    video = get_Video(file_path)

    assert video.num_frames == 143956

    video.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
    successful_read, _ = video.video.read()
    assert successful_read
    