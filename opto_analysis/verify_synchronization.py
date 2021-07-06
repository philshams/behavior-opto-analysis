import numpy as np
import cv2
import os



def verify_time_sync(file_paths: str, fps: int, DAQ_sampling_rate: int) -> None:

    
    # TODO: video data and then synchronize


    AI_file = os.path.join(folder_path + "analog1.bin")
    # contains two interposed 15 kHz time series
    AI_data = np.fromfile(AI_file)
    AI_num_samples = int(len(AI_data))

    AI_camera_data = AI_data[np.arange(0, AI_num_samples, 4)]
    AI_audio_data = AI_data[np.arange(1, AI_num_samples, 4)]

    # # predict number of frames from camera pulse
    # camera_pulse_on = np.diff(camera_pulse)
    # camera_pulse_on_idx = np.where(camera_pulse_on > 1)[0] + 1
    # number_of_frames_analog = len(camera_pulse_on_idx)
    # number_of_frames_analog_II = len(camera_pulse) / 15000 * fps

    # # open video and get number of frames
    video_file = os.path.join(folder_path + "cam1.avi")

    vid = cv2.VideoCapture(video_file)
    number_of_frames = vid.get(cv2.CAP_PROP_FRAME_COUNT)
    print(number_of_frames)

    # # did we get the right number of frames?
    # frames_not_in_analog = int(number_of_frames - number_of_frames_analog)
    # print('The video has ' + str(frames_not_in_analog) + ' more frames than the trigger signal')

    # # show the laser on video
    # pre_laser_frames = 3*fps
    # laser_duration_frames = laser_durations_pool * fps
    # post_laser_frames = 10*fps

    # for i, laser_onset_frame in enumerate(laser_onset_frames_pool):
    #     # set up save video
    #     video_save = cv2.VideoWriter("C:\\Users\\SWC\Desktop\\videos\\" + mouse_date + str(i+1) + ".mp4", cv2.VideoWriter_fourcc(*"XVID"), fps, (1024, 1024), True)

    #     # set saved video to start frame
    #     start_frame = laser_onset_frame - pre_laser_frames+frames_not_in_analog
    #     vid.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    #     # loop over frames
    #     for j in range(int(pre_laser_frames + laser_duration_frames[i] + post_laser_frames)):
    #         ret, frame = vid.read()
    #         frame_num = start_frame + j

    #         # print status on video
    #         if j <= pre_laser_frames:
    #             cv2.putText(frame, str(laser_durations[i]) + ' sec stim coming', (20, 50), 0, 1, (255, 255, 255), thickness=2)
    #         elif frame_num in laser_frames_all:
    #             cv2.putText(frame, '!!! - ' + str(laser_durations[i]) + ' sec stim ON - !!!', (20, 50), 0, 1, (100, 100, 255), thickness=2)
    #         elif (j-pre_laser_frames) >= laser_duration_frames[i]:
    #             cv2.putText(frame, 'Stimulus over', (20, 50), 0, 1, (255, 255, 255), thickness=2)
    #         else:
    #             cv2.putText(frame, 'another ' + str(laser_durations[i]) + ' sec stim coming', (20, 50), 0, 1, (255, 255, 255), thickness=2)

    #         cv2.imshow('LASER response', frame)
    #         video_save.write(frame)
    #         if cv2.waitKey(25) & 0xFF == ord('q'): break
    #     video_save.release()

    # check audio signal too !!!
    # stimulus_start_idx = stimulus_on_idx[np.append(np.ones(1).astype(bool), idx_since_last_stimulus_on > 2 * 10000)]  # usually 10 or 30
    # stimulus_start_frame = np.ceil(stimulus_start_idx / 10000 / (33 + 1 / 3) * 1000).astype(int)
    # stimulus_start_frame = stimulus_start_frame[stimulus_start_frame > 300]

    # print('done')

    # elif j < (pre_laser_frames + laser_durations[i]*fps):
    #     cv2.putText(frame, '!!! - ' + str(laser_durations[i]) + ' sec stim ON - !!!', (20, 50), 0, 1, (100, 100, 255), thickness=2)
