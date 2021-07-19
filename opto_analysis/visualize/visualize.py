from opto_analysis.track.register import load_fisheye_correction_map, correct_and_register_frame, generate_rendered_arena
from settings.visualization_settings import visualization_settings
import cv2
import numpy as np
import dill as pickle
import os

class Visualize():
    def __init__(self, session: object):
        self.source_video = cv2.VideoCapture(session.video.video_file)
        self.fisheye_correction_map = load_fisheye_correction_map(session.video)
        self.session = session
        with open(self.session.video.tracking_data_file, "rb") as dill_file: self.tracking_data = pickle.load(dill_file)
        self.save_folder = visualization_settings.save_folder
        self.size = visualization_settings.size
        self.rapid = visualization_settings.rapid
        self.rendering = visualization_settings.generate_rendering
        self.rapid = visualization_settings.rapid
        self.verbose = visualization_settings.verbose
        self.delay_between_frames = int(1000/self.session.video.fps*(not self.rapid)+self.rapid)
        self.onset_frames = {}
        self.onset_frames['laser'] = self.session.laser.onset_frames
        self.onset_frames['audio'] = self.session.audio.onset_frames
        self.stimulus_durations = {}
        self.stimulus_durations['laser'] = self.session.laser.stimulus_durations
        self.stimulus_durations['audio'] = self.session.audio.stimulus_durations

    def trials(self, stimulus_type, seconds_before, seconds_after):
        for trial_num, (onset_frames, stimulus_durations) in enumerate(zip(self.onset_frames[stimulus_type], self.stimulus_durations[stimulus_type])):
            self.set_up_videos(stimulus_type, trial_num, seconds_before, seconds_after, onset_frames, stimulus_durations)            
            for i in self.frames_in_this_trial:
                self.read_frame()
                self.correct_and_register_frame()
                self.display_stimulus_status_on_frame(i, stimulus_type)
                self.generate_rendering(i)
                self.display_and_save_frames(stimulus_type)
                if cv2.waitKey(self.delay_between_frames) & 0xFF == ord('q'): break # press q to quit this video
        self.release_video_objects()

    def read_frame(self):
        self.frame_num = int(self.source_video.get(cv2.CAP_PROP_POS_FRAMES))
        _, self.actual_frame = self.source_video.read()

    def correct_and_register_frame(self):
        self.actual_frame = correct_and_register_frame(self.actual_frame[:, :, 0], self.session.video, self.fisheye_correction_map)
    
    def display_stimulus_status_on_frame(self, i: int, stimulus_type: str) -> None:
        if self.verbose:    
            if self.stimulus_status[i]==0:
                cv2.putText(self.actual_frame, "{} stimulus - coming".format(stimulus_type), (60, 40), 0, 1, (150, 150, 150), thickness=2)
            elif self.stimulus_status[i]==1:
                cv2.putText(self.actual_frame, "{} stimulus - ON".format(stimulus_type), (60, 40), 0, 1, (255, 255, 255), thickness=2)
            elif self.stimulus_status[i]==2:
                cv2.putText(self.actual_frame, "{} stimulus - done".format(stimulus_type), (60, 40), 0, 1, (150, 150, 150), thickness=2)

    def generate_rendering(self, i):
        if i==0:
            self.initialize_rendered_frame()
        if self.rendering: 
            self.get_current_position_and_speed() 
            self.get_shading_color()
            self.shade_in_mouse_silhouette() 

    def display_and_save_frames(self, stimulus_type: str):
        cv2.imshow('{} stimulus effect - RAW'.format(stimulus_type), self.actual_frame)
        if self.rendering: cv2.imshow('{} stimulus effect - RENDER'.format(stimulus_type), self.rendered_frame)

        self.trial_video_raw.write(self.actual_frame)
        if self.rendering: self.trial_video_rendering.write(self.rendered_frame)

# ----------------------------------------------------------------------------------------------------------------

    def initialize_rendered_frame(self):
        self.rendered_frame = generate_rendered_arena(self.session, self.session.video.rendering_size_pixels)

    def get_current_position_and_speed(self):
        self.body_loc = self.tracking_data['body_loc'][self.frame_num, :]
        self.neck_loc = self.tracking_data['neck_loc'][self.frame_num, :]
        self.body_dir = self.tracking_data['body_dir'][self.frame_num]
        self.neck_dir = self.tracking_data['neck_dir'][self.frame_num]
        self.speed = self.tracking_data['speed'][self.frame_num]

    def get_shading_color(self):
        #                            corresponds to ----dark gray ----------dark blue--------medium blue-------------bright blue------------
        colors_slow_to_fast = [np.array(x) for x in [[254, 254, 254], [252.6, 253.5, 254], [240, 250, 254], [200, 250, 254], [200, 250, 254]]]
        speed_thresholds = np.array([0, 30, 45, 60, 999]) #cm/s
        assert self.speed < 999, "speed is unrealistically high"
        i = np.where( (self.speed - speed_thresholds)>0 )[0][-1] # index within the speed thresholds
        color_based_on_speed = ((speed_thresholds[i+1] - self.speed) * colors_slow_to_fast[i] + (self.speed - speed_thresholds[i]) * colors_slow_to_fast[i+1]) / (speed_thresholds[i+1] - speed_thresholds[i]) # somewhere between the darker and brighter color depending on its speed relative to the threshold speeds
        self.shading_color_light = 1 - (1 - color_based_on_speed / [255, 255, 255]) / (np.mean(1 - color_based_on_speed / [255, 255, 255]) / .08)
        self.shading_color_dark = (1 - (1 - color_based_on_speed / [255, 255, 255]) / (np.mean(1 - color_based_on_speed / [255, 255, 255]) / .38))**2

    def shade_in_mouse_silhouette(self) -> object:
        self.pixels_to_shade = np.zeros_like(self.rendered_frame)
        cv2.ellipse(self.pixels_to_shade, tuple(self.body_loc.astype(int)), (14, 8), 180-self.body_dir, 0, 360, 100, thickness=-1)

        # cv2.ellipse(self.pixels_to_shade, (479, 287), (14, 8), 180-self.body_dir, 0, 360, 100, thickness=-1)

        cv2.ellipse(self.pixels_to_shade, self.neck_loc, (11, 6), 180-self.neck_dir, 0, 360, 100, thickness=-1)

        self.rendered_frame[self.pixels_to_shade] = self.rendered_frame[self.pixels_to_shade] * self.shading_color

    def set_up_videos(self, stimulus_type: str, trial_num: int, seconds_before: float, seconds_after: float, onset_frames: object, stimulus_durations: object):
        assert stimulus_type in ['laser', 'audio'], "Stimulus type must be either 'laser' or 'audio'"
        self.source_video.set(cv2.CAP_PROP_POS_FRAMES, onset_frames[0]-seconds_before*self.session.video.fps) # set source video to trial start
        self.trial_video_raw = cv2.VideoWriter(os.path.join(self.save_folder, self.session.experiment, "{}-{}-{} trial {}-RAW.mp4".format(self.session.experiment, stimulus_type, self.session.mouse, trial_num+1)), cv2.VideoWriter_fourcc(*"mp4v"), self.session.video.fps, (self.size, self.size), False)
        if self.rendering: 
            self.trial_video_rendering = cv2.VideoWriter(os.path.join(self.save_folder, self.session.experiment, "{}-{}-{} trial {}-RENDER.mp4".format(self.session.experiment, stimulus_type, self.session.mouse, trial_num+1)), cv2.VideoWriter_fourcc(*"mp4v"), self.session.video.fps, (self.size, self.size), True)
        else:
            self.trial_video_rendering=None

        self.generate_stimulus_status_array(onset_frames, stimulus_durations, seconds_before, seconds_after, self.session.video.fps) # array: 0~pre-stimulus, 1~stimulus on, 2~stimulus done

        self.frames_in_this_trial = range((onset_frames[-1]-onset_frames[0])+int((seconds_before+stimulus_durations[-1]+seconds_after)*self.session.video.fps))

    def generate_stimulus_status_array(self, onset_frames: object, stimulus_durations: object, seconds_before: float, seconds_after: float, fps: int) -> object:
        self.stimulus_status = np.zeros((onset_frames[-1]-onset_frames[0])+int((seconds_before+stimulus_durations[-1]+seconds_after)*fps)) # 0 ~ stimulus is coming
        for onset_frame, stimulus_duration in zip(onset_frames, stimulus_durations):
            self.stimulus_status[int(seconds_before*fps+onset_frame-onset_frames[0]):int((seconds_before+stimulus_duration)*fps)+onset_frame-onset_frames[0]]=1 # 1 ~ stimulus is ON
        self.stimulus_status[-int(seconds_after*fps):]=2 # 2 ~ stimulus is done

    def release_video_objects(self):
        self.source_video.release()
        self.trial_video_raw.release()
        if self.rendering: self.trial_video_rendering.release()
        cv2.destroyAllWindows()
