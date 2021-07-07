from opto_analysis.process_data.session import Session
import cv2
import numpy as np

def verify_all_frames_saved(session: Session) -> None:
    assert session.camera_trigger.num_frames == session.video.num_frames, "---Video contains {} frames, but {} frames were triggered! (for experiment: {}, mouse: {})---".format(session.camera_trigger.num_frames, session.video.num_frames, session.experiment, session.mouse)

    print("Video frame synchronization correct for experiment: {}, mouse: {}".format(session.experiment, session.mouse))

def check_audio_sync(session:Session) -> None:
    # TODO: visualize audio trials, make sure timing looks right
    pass




def check_laser_sync(session: Session, seconds_before: float=4, seconds_after: float=4, rapid: bool=False) -> None:
    video_object =  cv2.VideoCapture(session.video.video_file)
    
    for onset_frames, stimulus_durations in zip(session.laser.onset_frames, session.laser.stimulus_durations):
        video_object.set(cv2.CAP_PROP_POS_FRAMES, onset_frames[0]-seconds_before*session.fps)
        # create laser status, an array with 0~pre-laser, 1~laser on, 2~laser done
        laser_status = generate_laser_status_array(onset_frames, stimulus_durations, seconds_before, seconds_after, session.fps)
        for i in range((onset_frames[-1]-onset_frames[0])+int((seconds_before+stimulus_durations[-1]+seconds_after)*session.fps)):
            _, frame = video_object.read()
            display_laser_status(stimulus_durations, laser_status[i], frame)
            cv2.imshow('laser effect', frame)
            if cv2.waitKey(int(1000/session.fps)) & 0xFF == ord('q'): break
        
    video_object.release()

    # TODO: check the syncing between laser and camera trigger; need to add 1500 samples delay to laser? Why are they off by 6000? Same for all session?

    # TODO: save video if desired
    # video_save = cv2.VideoWriter("C:\\Users\\SWC\Desktop\\videos\\" + mouse_date + str(i+1) + ".mp4", cv2.VideoWriter_fourcc(*"XVID"), fps, (1024, 1024), True)
    # video_save.release()


def display_laser_status(stimulus_durations: object, cur_laser_status: int, frame: object) -> None:
    if cur_laser_status==0:
        cv2.putText(frame, "{} s stimulus is coming".format(stimulus_durations[0]), (20, 40), 0, 1, (255, 255, 255), thickness=2)
    elif cur_laser_status==1:
        cv2.putText(frame, "{} sec stimulus is ON !!!".format(stimulus_durations[0]), (20, 40), 0, 1, (100, 100, 255), thickness=2)
    elif cur_laser_status==2:
        cv2.putText(frame, "Laser stimuli are done".format(stimulus_durations[0]), (20, 40), 0, 1, (255, 255, 255), thickness=2)

def generate_laser_status_array(onset_frames: object, stimulus_durations: object, seconds_before: float, seconds_after: float, fps: int) -> object:
    laser_status = np.zeros((onset_frames[-1]-onset_frames[0])+int((seconds_before+stimulus_durations[-1]+seconds_after)*fps)) # 0 ~ laser is coming
    for onset_frame, stimulus_duration in zip(onset_frames, stimulus_durations):
        laser_status[seconds_before*fps+onset_frame-onset_frames[0]:int((seconds_before+stimulus_duration)*fps)+onset_frame-onset_frames[0]]=1 # 1 ~ laser is ON
    laser_status[-int(seconds_after*fps):]=2 # 2 ~ laser is done
    return laser_status