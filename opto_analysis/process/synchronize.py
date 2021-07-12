from opto_analysis.process.session import Session

def verify_all_frames_saved(session: Session) -> None:
    assert session.camera_trigger.num_frames == session.video.num_frames, "---Video contains {} frames, but {} frames were triggered! (for experiment: {}, mouse: {})---".format(session.camera_trigger.num_frames, session.video.num_frames, session.experiment, session.mouse)

    print("All frames properly saved for experiment: {}".format(session.name))

def verify_aligned_data_streams(session: Session, known_offset: int = 6000) -> None:
    assert session.camera_trigger.num_samples == session.audio.num_samples and session.camera_trigger.num_samples == (session.laser.num_samples+known_offset), "---Data streams have mismatched numbers of samples---\nCamera trigger: {}\nAudio input: {}\nLaser output: {} = {} + {}".format(session.camera_trigger.num_samples, session.audio.num_samples, (session.laser.num_samples+known_offset), session.laser.num_samples, known_offset)

    print("Data streams properly synced for experiment {}".format(session.name))
