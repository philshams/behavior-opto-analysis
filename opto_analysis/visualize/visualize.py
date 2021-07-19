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
        assert os.path.isfile(self.session.video.tracking_data_file), 'Tracking data not found for session: {}'.format(session.name)
        with open(self.session.video.tracking_data_file, "rb") as dill_file: self.tracking_data = pickle.load(dill_file)
        self.save_folder = visualization_settings.save_folder
        self.size = visualization_settings.size
        self.rapid = visualization_settings.rapid
        self.rendering = visualization_settings.generate_rendering
        self.display_tracking = visualization_settings.display_tracking
        self.display_trail = visualization_settings.display_trail
        self.display_stim_info = visualization_settings.display_stim_status
        if self.display_tracking: self.video_type = 'TRACK'
        elif self.display_trail and not self.display_tracking: self.video_type = 'TRACE'
        else: self.video_type ='RAW'
        self.rapid = visualization_settings.rapid
        self.verbose = visualization_settings.display_stim_status
        self.delay_between_frames = int(1000/self.session.video.fps*(not self.rapid)+self.rapid)
        self.onset_frames = {}
        self.onset_frames['laser'] = self.session.laser.onset_frames
        self.onset_frames['audio'] = self.session.audio.onset_frames
        self.stimulus_durations = {}
        self.stimulus_durations['laser'] = self.session.laser.stimulus_durations
        self.stimulus_durations['audio'] = self.session.audio.stimulus_durations

    def trials(self, stimulus_type):
        for trial_num, (onset_frames, stimulus_durations) in enumerate(zip(self.onset_frames[stimulus_type], self.stimulus_durations[stimulus_type])):
            self.set_up_videos(stimulus_type, trial_num, onset_frames, stimulus_durations)            
            for i in self.frames_in_this_trial:
                self.read_frame(onset_frames)
                self.correct_and_register_frame()
                self.get_current_position_and_speed() 
                self.get_shading_color()
                self.display_stimulus_status_on_frame(i, stimulus_type)
                self.display_escape_trail_on_frame(i)
                self.display_tracking_on_frame(i)
                self.generate_rendering(i)
                self.display_and_save_frames(stimulus_type)
                if cv2.waitKey(self.delay_between_frames) & 0xFF == ord('q'): break # press q to quit this video
        self.release_video_objects()

    def read_frame(self, onset_frames):
        self.frame_num = int(self.source_video.get(cv2.CAP_PROP_POS_FRAMES))
        self.num_frames_past_stim = self.frame_num - onset_frames[0]
        _, self.actual_frame = self.source_video.read()

    def correct_and_register_frame(self):
        self.actual_frame = correct_and_register_frame(self.actual_frame[:, :, 0], self.session.video, self.fisheye_correction_map)
        if self.display_tracking or self.display_trail: self.actual_frame = cv2.cvtColor(self.actual_frame, cv2.COLOR_GRAY2RGB)
    
    def display_stimulus_status_on_frame(self, i: int, stimulus_type: str) -> None:
        if self.display_stim_info:   
            if self.stimulus_status[i]==1: 
                if stimulus_type == 'laser': 
                    cv2.putText(self.actual_frame, "!", (self.avg_loc[0] - 100, self.avg_loc[1] - 40), 4, 1.5, (255,200,0), thickness=6)
                elif self.display_tracking:
                    cv2.putText(self.actual_frame, "!", (self.avg_loc[0] - 100, self.avg_loc[1] - 40), 4, 1.5, (255,255,255), thickness=6)
                else:
                    cv2.putText(self.actual_frame, "!", (self.avg_loc[0] - 100, self.avg_loc[1] - 40), 4, 1.5, (100,200,255), thickness=6)
                cv2.putText(self.actual_frame, "!", (self.avg_loc[0] - 100, self.avg_loc[1] - 40), 4, 1.5, (0,0,0), thickness=4)

    def get_current_position_and_speed(self):
        if self.rendering or self.display_tracking or self.display_trail or self.display_stim_info:
            self.body_loc = self.tracking_data['body_loc'][self.frame_num, :]
            self.neck_loc = self.tracking_data['neck_loc'][self.frame_num, :]
            self.body_dir = self.tracking_data['body_dir'][self.frame_num]
            self.neck_dir = self.tracking_data['neck_dir'][self.frame_num]
            self.speed = self.tracking_data['speed'][self.frame_num]
            self.avg_loc = (int(self.tracking_data['avg_loc'][self.frame_num, 0]), int(self.tracking_data['avg_loc'][self.frame_num, 1]))
            
    def get_shading_color(self):
        speed_thresholds = np.array([0, 20, 40, 70, 999]) #cm/s
        if self.rendering:
            shading_colors = [np.array(x) for x in [[254, 254, 254], [254, 253.5, 252.6], [254, 250, 240], [254, 250, 200], [200, 250, 254]]]
            i = np.where( (self.speed - speed_thresholds)>0 )[0][-1] # index within the speed thresholds
            shading_color_based_on_speed = ((speed_thresholds[i+1] - self.speed) * shading_colors[i] + (self.speed - speed_thresholds[i]) * shading_colors[i+1]) / (speed_thresholds[i+1] - speed_thresholds[i]) # somewhere between the darker and brighter color depending on its speed relative to the threshold speeds
            self.shading_color_light = 1 - (1 - shading_color_based_on_speed / [255, 255, 255]) / (np.mean(1 - shading_color_based_on_speed / [255, 255, 255]) / .08)
            self.shading_color_dark = (1 - (1 - shading_color_based_on_speed / [255, 255, 255]) / (np.mean(1 - shading_color_based_on_speed / [255, 255, 255]) / .38))**2
        if self.display_tracking or self.display_trail:
            escape_trail_colors = [np.array(x) for x in [[50,50,50], [50,50,100], [50, 100, 200], [250, 250, 255], [250, 250, 255]]]
            speed_text_colors   = [np.array(x) for x in [[100,100,100], [100,100,175], [100, 175, 220], [250, 250, 255], [250, 250, 255]]]

            i = np.where( (self.speed - speed_thresholds)>0 )[0][-1] # index within the speed thresholds
            self.escape_trail_color = ((speed_thresholds[i+1] - self.speed) * escape_trail_colors[i] + (self.speed - speed_thresholds[i]) * escape_trail_colors[i+1]) / (speed_thresholds[i+1] - speed_thresholds[i]) # somewhere between the darker and brighter color depending on its speed relative to the threshold speeds

            self.speed_text_color = ((speed_thresholds[i+1] - self.speed) * speed_text_colors[i] + (self.speed - speed_thresholds[i]) * speed_text_colors[i+1]) / (speed_thresholds[i+1] - speed_thresholds[i]) 

    def display_escape_trail_on_frame(self, i):
        if self.display_trail:
            for j, (dot_loc, dot_color) in enumerate(zip(self.trail_of_dots, self.trail_of_dots_colors)):
                # if j: cv2.line(self.actual_frame, dot_loc, self.trail_of_dots[j-1], (220,220,220),thickness=1, lineType=16)
                if j: cv2.line(self.actual_frame, dot_loc, self.trail_of_dots[j-1], dot_color, thickness=2, lineType=16)

            if self.num_frames_past_stim % 15 and self.stimulus_status[i]==1:
                self.trail_of_dots.append(self.avg_loc)
                self.trail_of_dots_colors.append(self.escape_trail_color)

    def display_tracking_on_frame(self, i):
        if self.display_tracking:
            self.display_avg_location_on_frame()
            self.display_speed_on_frame()
            self.display_heading_dir_on_frame()
            self.display_colored_dot_for_each_bodypart_on_frame()

    def generate_rendering(self, i):
        if self.rendering: 
            if i==0: self.initialize_rendered_frame()
            self.shade_in_mouse_silhouette() 

    def display_and_save_frames(self, stimulus_type: str):
        cv2.imshow('{} stimulus effect - RAW'.format(stimulus_type), self.actual_frame)
        if self.rendering: cv2.imshow('{} stimulus effect - RENDER'.format(stimulus_type), self.rendered_frame)

        self.trial_video_raw.write(self.actual_frame)
        if self.rendering: self.trial_video_rendering.write(self.rendered_frame)

# ----------------------------------------------------------------------------------------------------------------

    def initialize_rendered_frame(self):
        self.rendered_frame, _ = generate_rendered_arena(self.session, self.session.video.rendering_size_pixels)
        self.rendered_frame = cv2.cvtColor(self.rendered_frame, cv2.COLOR_GRAY2RGB)

    def shade_in_mouse_silhouette(self) -> object:
        self.pixels_to_shade = np.zeros(self.rendered_frame.shape[:2])
        cv2.ellipse(self.pixels_to_shade, tuple(self.body_loc.astype(int)), (14, 8), 180-self.body_dir, 0, 360, (255,255,255), thickness=-1)
        cv2.ellipse(self.pixels_to_shade, tuple(self.neck_loc.astype(int)), (11, 6), 180-self.neck_dir, 0, 360, (255,255,255), thickness=-1)

        self.rendered_frame[self.pixels_to_shade.astype(bool)] = self.rendered_frame[self.pixels_to_shade.astype(bool)] * self.shading_color_light

# ----------------------------------------------------------------------------------------------------------------

      
    def display_avg_location_on_frame(self):
        cv2.circle(self.actual_frame, self.avg_loc, 3, (220,220,220), -1)

    def display_speed_on_frame(self):
        cv2.putText(self.actual_frame, '{} cm/s'.format(np.round(self.speed)), (self.actual_frame.shape[1]-200, 45), 0, 1, self.speed_text_color, thickness=2)

    def display_heading_dir_on_frame(self):
        heading_dir_x =  int(30*np.cos(np.deg2rad(self.body_dir)))
        heading_dir_y = -int(30*np.sin(np.deg2rad(self.body_dir)))
        cv2.arrowedLine(self.actual_frame, self.avg_loc, (self.avg_loc[0] + heading_dir_x, self.avg_loc[1] + heading_dir_y), (220,220,220), 1, 16)

    def display_colored_dot_for_each_bodypart_on_frame(self):
        bodypart_colors = [(0, 0, 255),(255, 0, 255),(120, 120, 255),(0, 255, 255),(0, 255, 150),(0, 150, 0),(255, 255, 0),(120,120,120),(255, 50, 0),(255, 50, 80),(255, 50, 150),(150, 0, 150),(30, 0, 180)]

        for j, (bodypart, color) in enumerate(zip(self.tracking_data['bodyparts'], bodypart_colors)):
            bodypart_loc = (int(self.tracking_data[bodypart][self.frame_num, 0]), int(self.tracking_data[bodypart][self.frame_num, 1]))
            cv2.circle(self.actual_frame, bodypart_loc, 1, color, -1)
            cv2.putText(self.actual_frame, bodypart, (self.actual_frame.shape[0] - 85, self.actual_frame.shape[1] - 280 + j * 20), 0, .4, color, thickness=1)

# ----------------------------------------------------------------------------------------------------------------

    def set_up_videos(self, stimulus_type: str, trial_num: int, onset_frames: object, stimulus_durations: object):
        assert stimulus_type in ['laser', 'audio'], "Stimulus type must be either 'laser' or 'audio'"
        if stimulus_type=='laser':
            self.seconds_before = visualization_settings.seconds_before_laser
            self.seconds_after = visualization_settings.seconds_after_laser
        if stimulus_type=='audio':
            self.seconds_before = visualization_settings.seconds_before_audio
            self.seconds_after = visualization_settings.seconds_after_audio

        self.source_video.set(cv2.CAP_PROP_POS_FRAMES, onset_frames[0]-self.seconds_before*self.session.video.fps) # set source video to trial start
        self.trial_video_raw = cv2.VideoWriter(os.path.join(self.save_folder, self.session.experiment, "{}-{}-{} trial {}-{}.mp4".format(self.session.experiment, stimulus_type, self.session.mouse, trial_num+1, self.video_type)), cv2.VideoWriter_fourcc(*"mp4v"), self.session.video.fps, (self.size, self.size), self.display_tracking or self.display_trail)
        if self.rendering: 
            self.trial_video_rendering = cv2.VideoWriter(os.path.join(self.save_folder, self.session.experiment, "{}-{}-{} trial {}-RENDER.mp4".format(self.session.experiment, stimulus_type, self.session.mouse, trial_num+1)), cv2.VideoWriter_fourcc(*"mp4v"), self.session.video.fps, (self.size, self.size), True)
        else:
            self.trial_video_rendering=None

        self.generate_stimulus_status_array(onset_frames, stimulus_durations, self.session.video.fps) # array: 0~pre-stimulus, 1~stimulus on, 2~stimulus done

        self.frames_in_this_trial = range((onset_frames[-1]-onset_frames[0])+int((self.seconds_before+stimulus_durations[-1]+self.seconds_after)*self.session.video.fps))

        self.trail_of_dots = []
        self.trail_of_dots_colors = []

    def generate_stimulus_status_array(self, onset_frames: object, stimulus_durations: object, fps: int) -> object:
        self.stimulus_status = np.zeros((onset_frames[-1]-onset_frames[0])+int((self.seconds_before+stimulus_durations[-1]+self.seconds_after)*fps)) # 0 ~ stimulus is coming
        for onset_frame, stimulus_duration in zip(onset_frames, stimulus_durations):
            self.stimulus_status[int(self.seconds_before*fps+onset_frame-onset_frames[0]):int((self.seconds_before+stimulus_duration)*fps)+onset_frame-onset_frames[0]]=1 # 1 ~ stimulus is ON
        self.stimulus_status[-int(self.seconds_after*fps):]=2 # 2 ~ stimulus is done

    def release_video_objects(self):
        self.source_video.release()
        self.trial_video_raw.release()
        if self.rendering: self.trial_video_rendering.release()
        cv2.destroyAllWindows()
