from opto_analysis.process_data.session import Session
import cv2
import numpy as np

def verify_all_frames_saved(session: Session) -> None:
    assert session.camera_trigger.num_frames == session.video.num_frames, "---Video contains {} frames, but {} frames were triggered! (for experiment: {}, mouse: {})---".format(session.camera_trigger.num_frames, session.video.num_frames, session.experiment, session.mouse)

    print("All frames properly saved for experiment {}".format(session.name))

def check_stimulus_sync(session:Session, stimulus_type: str='laser', seconds_before: float=4, seconds_after: float=4, rapid: bool=False) -> None:
    assert stimulus_type in ['laser', 'audio'], "Stimulus type must be either 'laser' or 'audio'"

    video_object =  cv2.VideoCapture(session.video.video_file)
    
    for onset_frames, stimulus_durations in zip(session.__dict__[stimulus_type].onset_frames, session.__dict__[stimulus_type].stimulus_durations):

        video_object.set(cv2.CAP_PROP_POS_FRAMES, onset_frames[0]-seconds_before*session.fps)
        # create stimulus status, an array with 0~pre-stimulus, 1~stimulus on, 2~stimulus done
        stimulus_status = generate_stimulus_status_array(onset_frames, stimulus_durations, seconds_before, seconds_after, session.fps)
        for i in range((onset_frames[-1]-onset_frames[0])+int((seconds_before+stimulus_durations[-1]+seconds_after)*session.fps)):
            _, frame = video_object.read()
            display_stimulus_status(stimulus_durations, stimulus_status[i], frame, stimulus_type)
            if stimulus_status[i]==1:
                x=0
            cv2.imshow('{} stimulus effect'.format(stimulus_type), frame)
            if cv2.waitKey(int(1000/session.fps*(not rapid)+rapid)) & 0xFF == ord('q'): break
        
    video_object.release()

    # TODO: check the syncing between laser and camera trigger; need to add 1500 samples delay to laser? Why are they off by 6000? Same for all session
    
def display_stimulus_status(stimulus_durations: object, cur_stimulus_status: int, frame: object, stimulus_type: str) -> None:
    if cur_stimulus_status==0:
        cv2.putText(frame, "{} s {} stimulus is coming".format(stimulus_durations[0], stimulus_type), (20, 40), 0, 1, (255, 255, 255), thickness=2)
    elif cur_stimulus_status==1:
        cv2.putText(frame, "{} s {} stimulus is ON !!!".format(stimulus_durations[0], stimulus_type), (20, 40), 0, 1, (100, 100, 255), thickness=2)
    elif cur_stimulus_status==2:
        cv2.putText(frame, "{} stimulus is done".format(stimulus_type), (20, 40), 0, 1, (255, 255, 255), thickness=2)

def generate_stimulus_status_array(onset_frames: object, stimulus_durations: object, seconds_before: float, seconds_after: float, fps: int) -> object:
    stimulus_status = np.zeros((onset_frames[-1]-onset_frames[0])+int((seconds_before+stimulus_durations[-1]+seconds_after)*fps)) # 0 ~ stimulus is coming
    for onset_frame, stimulus_duration in zip(onset_frames, stimulus_durations):
        stimulus_status[seconds_before*fps+onset_frame-onset_frames[0]:int((seconds_before+stimulus_duration)*fps)+onset_frame-onset_frames[0]]=1 # 1 ~ stimulus is ON
    stimulus_status[-int(seconds_after*fps):]=2 # 2 ~ stimulus is done
    return stimulus_status