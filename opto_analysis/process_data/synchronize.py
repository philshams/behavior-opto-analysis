


from opto_analysis.process_data.session import Session

def verify_all_frames_saved(session: Session) -> None:
    assert session.camera_trigger.num_frames == session.video.num_frames, "---Video contains {} frames, but {} frames were triggered! (for experiment: {}, mouse: {})---".format(session.camera_trigger.num_frames, session.video.num_frames, session.experiment, session.mouse)

    print("Video frame synchronization correct for experiment: {}, mouse: {}".format(session.experiment, session.mouse))

def check_audio_sync(session:Session) -> None:
    # TODO: visualize audio trials, make sure timing looks right
    pass




def check_laser_sync(session: Session) -> None:
    # TODO: visualize laser trials, make sure timing looks right
    pass


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
