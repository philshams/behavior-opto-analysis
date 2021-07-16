def dlc_tracking(session: object, tracking_settings: object) -> None:
    from deeplabcut.pose_estimation_tensorflow import analyze_videos
    analyze_videos(tracking_settings.dlc_settings_file, session.video.video_file)
    