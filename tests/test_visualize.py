from opto_analysis.visualize.visualize import Visualize
from opto_analysis.process.process import Process
from opto_analysis.run import collect_session_IDs
from sample_data.sample_databank import databank
from sample_data.sample_settings.sample_settings_visualize import settings_visualize
import numpy as np
import cv2
import os

def test_visualize_trials():
    selected_session_IDs = collect_session_IDs(settings_visualize, databank)
    session = Process(selected_session_IDs[0]).load_session()

    visualize = Visualize(session, settings_visualize)
    i = 0
    trial_num = 0
    for stimulus_type in ['audio','laser']:
        onset_frames = visualize.onset_frames[stimulus_type][0]
        stimulus_durations = visualize.stimulus_durations[stimulus_type][0]
        set_up_videos_assertions(visualize, stimulus_type, trial_num, onset_frames, stimulus_durations)
        read_frame_assertions(visualize, onset_frames)
        correct_and_register_frame_assertions(visualize)
        get_current_position_and_speed_assertions(visualize) 
        get_shading_color_assertions(visualize)
        visualize.display_stimulus(i, stimulus_type) # test in test_visualize
        visualize.display_trail(i) # test in test_visualize
        visualize.display_tracking(i)
        visualize.generate_rendering(i)
        visualize.display_and_save_frames(stimulus_type)
        cv2.waitKey(visualize.delay_between_frames)
        release_video_objects_assertions(visualize, stimulus_type)

def set_up_videos_assertions(visualize, stimulus_type, trial_num, onset_frames, stimulus_durations):
    visualize.set_up_videos(stimulus_type, trial_num, onset_frames, stimulus_durations)
    assert not visualize.trial_video_raw == None
    assert visualize.trial_video_rendering == None

def read_frame_assertions(visualize, onset_frames):
    visualize.read_frame(onset_frames)
    assert visualize.successful_read
    assert visualize.frame_num == onset_frames[0] - visualize.session.video.fps  * visualize.seconds_before

def correct_and_register_frame_assertions(visualize):
    visualize.correct_and_register_frame()
    assert np.sum(visualize.actual_frame)==240630834 or np.sum(visualize.actual_frame)==234652902

def get_current_position_and_speed_assertions(visualize):
    visualize.get_current_position_and_speed()
    assert visualize.body_dir == 76.55667655549335 or visualize.body_dir == 10.562744077609219

def get_shading_color_assertions(visualize):
    visualize.get_shading_color()
    assert (visualize.trail_color==np.array([50., 50., 81.29885662039507])).all() \
        or (visualize.speed_text_color==np.array([100.0, 100.0, 150.16538231641042])).all()

def release_video_objects_assertions(visualize, stimulus_type):
    visualize.release_video_objects()
    saved_video_file = os.path.join(visualize.save_folder, visualize.session.experiment, "{}-{}-{} trial {}-{}.mp4".format(visualize.session.experiment, stimulus_type, visualize.session.mouse, 1, visualize.video_type))
    saved_video = cv2.VideoCapture(saved_video_file)
    successful_read, _ = saved_video.read()
    assert successful_read
    saved_video.release()
    os.remove(saved_video_file)
