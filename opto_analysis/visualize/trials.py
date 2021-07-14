from opto_analysis.registration import load_fisheye_correction_map, correct_and_register_frame
from typing import Tuple
import cv2
import numpy as np
import os

def visualize_trials(session: object, visualization_settings: object, stimulus_type: str='laser', seconds_before: float=4, seconds_after: float=4, rapid: bool=False, verbose: bool=True, rendering: bool=False) -> None:
    
    assert stimulus_type in ['laser', 'audio'], "Stimulus type must be either 'laser' or 'audio'"

    source_video =  cv2.VideoCapture(session.video.video_file)
    fisheye_correction_map = load_fisheye_correction_map(session.video)

    for trial_num, (onset_frames, stimulus_durations) in enumerate(zip(session.__dict__[stimulus_type].onset_frames, session.__dict__[stimulus_type].stimulus_durations)):

        source_video.set(cv2.CAP_PROP_POS_FRAMES, onset_frames[0]-seconds_before*session.video.fps) # set to trial start

        trial_video_raw, trial_video_rendering = set_up_videos_to_save(session, visualization_settings, stimulus_type, trial_num)

        stimulus_status = generate_stimulus_status_array(onset_frames, stimulus_durations, seconds_before, seconds_after, session.video.fps) # create an array with 0~pre-stimulus, 1~stimulus on, 2~stimulus done
        
        for i in range((onset_frames[-1]-onset_frames[0])+int((seconds_before+stimulus_durations[-1]+seconds_after)*session.video.fps)):
            _, frame = source_video.read()
            frame = correct_and_register_frame(frame[:, :, 0], session.video, fisheye_correction_map)
            if verbose: display_stimulus_status(stimulus_durations, stimulus_status[i], frame, stimulus_type)
            if rendering: pass
            cv2.imshow('{} stimulus effect'.format(stimulus_type), frame)
            trial_video_raw.write(frame)
            if rendering: trial_video_rendering.write(rendering)
            if cv2.waitKey(int(1000/session.video.fps*(not rapid)+rapid)) & 0xFF == ord('q'): break
        
    source_video.release()
    trial_video_raw.release()
    if rendering:trial_video_rendering.release()



def set_up_videos_to_save(session: object, visualization_settings: object, stimulus_type: str, trial_num: int) -> Tuple[object, object, object]:

    trial_video_raw = cv2.VideoWriter(os.path.join(visualization_settings.save_folder, session.experiment, "{}-{}-{} trial {}-RAW.mp4".format(session.experiment, stimulus_type, session.mouse, trial_num+1)), cv2.VideoWriter_fourcc(*"mp4v"), session.video.fps, (visualization_settings.size, visualization_settings.size), False)

    if visualization_settings.generate_rendering: trial_video_rendering = cv2.VideoWriter(os.path.join(visualization_settings.save_folder, session.experiment, "{}-{}-{} trial {}-RENDER.mp4".format(session.experiment, stimulus_type, session.mouse, trial_num+1)), cv2.VideoWriter_fourcc(*"mp4v"), session.video.fps, (visualization_settings.size, visualization_settings.size), True)
    else: trial_video_rendering=None

    return trial_video_raw, trial_video_rendering

def display_stimulus_status(stimulus_durations: object, cur_stimulus_status: int, frame: object, stimulus_type: str) -> None:
    if cur_stimulus_status==0:
        cv2.putText(frame, "{} stimulus - coming".format(stimulus_type), (60, 40), 0, 1, (150, 150, 150), thickness=2)
    elif cur_stimulus_status==1:
        cv2.putText(frame, "{} stimulus - ON".format(stimulus_type), (60, 40), 0, 1, (255, 255, 255), thickness=2)
    elif cur_stimulus_status==2:
        cv2.putText(frame, "{} stimulus - done".format(stimulus_type), (60, 40), 0, 1, (150, 150, 150), thickness=2)

def generate_stimulus_status_array(onset_frames: object, stimulus_durations: object, seconds_before: float, seconds_after: float, fps: int) -> object:
    stimulus_status = np.zeros((onset_frames[-1]-onset_frames[0])+int((seconds_before+stimulus_durations[-1]+seconds_after)*fps)) # 0 ~ stimulus is coming
    for onset_frame, stimulus_duration in zip(onset_frames, stimulus_durations):
        stimulus_status[int(seconds_before*fps+onset_frame-onset_frames[0]):int((seconds_before+stimulus_duration)*fps)+onset_frame-onset_frames[0]]=1 # 1 ~ stimulus is ON
    stimulus_status[-int(seconds_after*fps):]=2 # 2 ~ stimulus is done
    return stimulus_status