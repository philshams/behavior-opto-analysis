import numpy as np
# import matplotlib.pyplot as plt
import cv2
import os
# import itertools


#! this is an alert
#? this is a query
#* this is important
#TODO: this is a todo
  

def verify_time_sync(folder_prefix: str, file_paths: list):

    for folder_path in [folder_prefix + fp for fp in file_paths]:

        analog_signal_file = os.path.join(folder_path + "analog1.bin")
        video_file = os.path.join(folder_path + "cam1.avi")
        laser_file = os.path.join(folder_path + "laser_fire1.bin")

        # open analog signal (frames and sound) and count the frames
        analog_signal = np.fromfile(analog_signal_file) 
        total_length = int(len(analog_signal))
        print(total_length)






        # camera_pulse = analog_signal[np.arange(0,total_length,4)] # subtract buffer of 3000
        # audio_signal = analog_signal[np.arange(1,total_length,4)] # now at 15kHz
        # fps = 40

        # # open laser signal and tell when the laser comes on
        laser_signal = np.fromfile(laser_file) # at 15 kHz
        if np.sum(laser_signal)==0:
            print('No laser stims in this session')
            continue
        else: print('Laser detected')
        # laser_on = np.diff(laser_signal)
        # laser_on_idx = np.where(laser_on > .2)[0] + 1
        # time_since_last_laser_pulse = np.diff(laser_on_idx)

        # # get the idx of the laser onset and how long the stimulation lasted
        # groups = []; laser_durations = []; laser_onset_idx = []; idx = 0
        # for k, g in itertools.groupby(time_since_last_laser_pulse):
        #     # print(k)
        #     #
        #     groups.append(list(g))
        #     group_length = len(groups[-1]);
        #     if k < 2000:  # not including ITI
        #         laser_durations.append(np.round(k * group_length / 15000))
        #         laser_onset_idx.append(laser_on_idx[idx])
        #     idx += group_length

        # laser_onset_frames = np.round(np.array(laser_onset_idx) / 15000 * fps).astype(int)
        # # laser_frames_all = np.array([np.arange(LOF, LOF + LD*fps) for LOF, LD in zip(laser_onset_frames, laser_durations)]).flatten()
        # laser_frames_all = np.array(list(flatten([list(np.arange(LOF, LOF + LD * fps)) for LOF, LD in zip(laser_onset_frames, laser_durations)])))

        # # get how many pulses were sent (i.e. laser onset within 10 secs)
        # max_ILI = 10
        # time_between_pulses = np.append(np.ones(1)*np.inf,np.diff(laser_onset_frames)/fps)
        # laser_onset_frames_pool = laser_onset_frames[time_between_pulses > max_ILI]
        # laser_durations_pool = np.array(laser_durations)[time_between_pulses > max_ILI]
        # laser_number_stims = np.ones_like(laser_onset_frames_pool)

        # i_pool = -1
        # for i, ILI in enumerate(time_between_pulses): # add the ILI to stims with other stims right after
        #     if ILI < max_ILI:
        #         laser_durations_pool[i_pool] += time_between_pulses[i]
        #         laser_number_stims[i_pool] += 1
        #     else:
        #         i_pool += 1


        # print(laser_onset_frames_pool / fps / 60)
        # print(laser_durations_pool)

        # # predict number of frames from camera pulse
        # camera_pulse_on = np.diff(camera_pulse)
        # camera_pulse_on_idx = np.where(camera_pulse_on > 1)[0] + 1
        # number_of_frames_analog = len(camera_pulse_on_idx)
        # number_of_frames_analog_II = len(camera_pulse) / 15000 * fps

        # # open video and get number of frames
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







