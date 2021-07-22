from opto_analysis.utils.open_tracking_data import open_tracking_data
from opto_analysis.track.register import load_fisheye_correction_map, correct_and_register_frame
import cv2
import numpy as np
import os

class Visualize():
    def __init__(self, session: object, settings: object):
        self.session = session
        self.fisheye_correction_map = load_fisheye_correction_map(session.video)
        self.size = settings.size
        self.rapid = settings.rapid
        self.display_tracking_option = settings.display_tracking
        self.display_trail_option = settings.display_trail
        self.display_stimulus_option = settings.display_stim_status
        self.rapid = settings.rapid
        self.verbose = settings.display_stim_status
        self.delay_between_frames = int(1000/self.session.video.fps*(not self.rapid)+self.rapid)
        self.onset_frames = {}
        self.onset_frames['laser'] = self.session.laser.onset_frames
        self.onset_frames['audio'] = self.session.audio.onset_frames
        self.stimulus_durations = {}
        self.stimulus_durations['laser'] = self.session.laser.stimulus_durations
        self.stimulus_durations['audio'] = self.session.audio.stimulus_durations
        open_tracking_data(self)

    def trials(self, stimulus_type):
        for trial_num, (onset_frames, stimulus_durations) in enumerate(zip(self.onset_frames[stimulus_type], self.stimulus_durations[stimulus_type])):
            self.set_up_videos(stimulus_type, trial_num, onset_frames, stimulus_durations)            
            for i in self.frames_in_this_trial:
                self.read_frame(onset_frames)
                self.correct_and_register_frame()
                self.get_current_position_and_speed() 
                self.get_shading_color(i)
                self.display_stimulus(i)
                self.display_trail(i)
                self.display_tracking(i)
                self.display_and_save_frames()
                key = cv2.waitKey(self.delay_between_frames)
                if key == ord('q'): break
            if key == ord('q'): break
        self.release_video_objects()

# -----FIRST-LEVEL FUNCTIONS---------------------------------------------------------------------------------------

    def read_frame(self, onset_frames):
        self.frame_num = int(self.source_video.get(cv2.CAP_PROP_POS_FRAMES))
        self.num_frames_past_stim = self.frame_num - onset_frames[0]
        self.successful_read, self.actual_frame = self.source_video.read()

    def correct_and_register_frame(self):
        self.actual_frame = correct_and_register_frame(self.actual_frame[:, :, 0], self.session.video, self.fisheye_correction_map)
        if self.display_tracking_option or self.display_trail_option: self.actual_frame = cv2.cvtColor(self.actual_frame, cv2.COLOR_GRAY2RGB)
    
    def get_current_position_and_speed(self):
        if self.display_tracking_option or self.display_trail_option or self.display_stimulus_option:
            self.body_dir = self.tracking_data['body_dir'][self.frame_num]
            self.speed = self.tracking_data['speed'][self.frame_num]
            self.avg_loc = (int(self.tracking_data['avg_loc'][self.frame_num, 0]), int(self.tracking_data['avg_loc'][self.frame_num, 1]))

    def get_shading_color(self, i):
        if   self.stimulus_type == 'audio': speed_thresholds = np.array([0, 20, 40, 70, 999]) #cm/s
        elif self.stimulus_type == 'laser': speed_thresholds = np.array([0, 15, 20, 30, 999]) #cm/s
        if self.display_trail_option:
            if   self.stimulus_type=='audio': 
                trail_colors = [np.array(x) for x in [[50,50,50], [50,50,100], [50, 100, 200], [250, 250, 255], [250, 250, 255]]]
            elif self.stimulus_type=='laser' and self.stimulus_status[i] != 0: 
                trail_colors = [np.array(x) for x in [[25,25,25], [100,50,50], [200, 100, 50], [255, 230, 230], [255, 230, 230]]]
            elif self.stimulus_type=='laser' and self.stimulus_status[i] == 0:
                trail_colors = [np.array(x) for x in [[255, 200, 0], [255, 200, 0], [255, 200, 0], [255, 200, 0], [255, 200, 0]]]
            self.trail_color = self.compute_intermediate_color_based_on_speed(speed_thresholds, trail_colors)
        if self.display_tracking_option: 
            speed_text_colors = [np.array(x) for x in [[100,100,100], [100,100,175], [100, 175, 220], [250, 250, 255], [250, 250, 255]]]
            self.speed_text_color = self.compute_intermediate_color_based_on_speed(speed_thresholds, speed_text_colors)

    def display_stimulus(self, i: int) -> None:
        if self.display_stimulus_option and self.stimulus_status[i]==0 and (self.stimulus_type=='audio' or (self.stimulus_type=='laser' and self.display_tracking_option)):
            if self.stimulus_type == 'laser': exclamation_color = (255, 200, 0)
            else: exclamation_color = (100,200,255)
            cv2.putText(self.actual_frame, "!", (self.avg_loc[0] - 100, self.avg_loc[1] - 40), 4, 1.5, exclamation_color, thickness=6)
            cv2.putText(self.actual_frame, "!", (self.avg_loc[0] - 100, self.avg_loc[1] - 40), 4, 1.5, (0,0,0), thickness=4)

    def display_trail(self, i):
        if self.display_trail_option:
            for j, (line, line_color, line_thickness) in enumerate(zip(self.trail, self.trail_colors, self.trail_thicknesses)):
                if j: cv2.line(self.actual_frame, line, self.trail[j-1], line_color, thickness=line_thickness, lineType=16)
            if self.num_frames_past_stim % 10 and ((self.stimulus_type=='audio' and self.stimulus_status[i]==0) or \
                        (self.stimulus_type=='laser' and self.stimulus_status[i] > -1 and self.stimulus_status[i] < 3)):
                self.trail.append(self.avg_loc)
                self.trail_colors.append(self.trail_color)
                self.trail_thicknesses.append(int(self.stimulus_status[i]!=0)+int(self.stimulus_type=='audio')+1)

    def display_tracking(self, i):
        if self.display_tracking_option:
            self.display_avg_location_on_frame()
            self.display_speed_on_frame()
            self.display_heading_dir_on_frame()
            self.display_colored_dot_for_each_bodypart_on_frame()

    def display_and_save_frames(self):
        cv2.imshow('{} stimulus effect'.format(self.stimulus_type), self.actual_frame)
        self.trial_video.write(self.actual_frame)

# -----TRACKING DISPLAY FUNCTIONS-----------------------------------------------------------------------------------
      
    def compute_intermediate_color_based_on_speed(self, speed_thresholds, colors):
        i = np.where( (self.speed - speed_thresholds)>0 )[0][-1]
        intermediate_color = ((speed_thresholds[i+1] - self.speed) * colors[i] + (self.speed - speed_thresholds[i]) * colors[i+1]) / (speed_thresholds[i+1] - speed_thresholds[i])
        return intermediate_color

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

# ----SETUP FUNCTIONS-----------------------------------------------------------------------------------------------

    def set_up_videos(self, stimulus_type: str, trial_num: int, onset_frames: object, stimulus_durations: object):
        self.stimulus_durations = stimulus_durations
        self.stimulus_type = stimulus_type
        self.onset_frames = onset_frames
        self.fps = self.session.video.fps

        assert self.stimulus_type in ['laser', 'audio'], "Stimulus type must be either 'laser' or 'audio'"
        if self.stimulus_type=='laser':
            self.seconds_before = self.settings.seconds_before_laser
            self.seconds_after = self.settings.seconds_after_laser
        if self.stimulus_type=='audio':
            self.seconds_before = self.settings.seconds_before_audio
            self.seconds_after = self.settings.seconds_after_audio

        if self.display_tracking_option: self.video_type = 'tracking'
        else: self.video_type = self.stimulus_type

        self.source_video = cv2.VideoCapture(self.session.video.video_file)
        self.source_video.set(cv2.CAP_PROP_POS_FRAMES, onset_frames[0]-self.seconds_before*self.session.video.fps) # set source video to trial start
        self.trial_video = cv2.VideoWriter(os.path.join(self.settings.save_folder, self.session.experiment,self.video_type, "{}-{}-{}-{}.mp4".format(self.session.experiment, self.session.mouse, self.stimulus_type, trial_num+1)), cv2.VideoWriter_fourcc(*"mp4v"), self.session.video.fps, (self.size, self.size), self.display_tracking_option or self.display_trail_option)

        self.generate_stimulus_status_array() # array: 0~pre-stimulus, 1~stimulus on, 2~stimulus done

        self.frames_in_this_trial = range((onset_frames[-1]-onset_frames[0])+int((self.seconds_before+stimulus_durations[-1]+self.seconds_after)*self.session.video.fps))

        self.trail = []
        self.trail_colors = []
        self.trail_thicknesses = []

    def generate_stimulus_status_array(self) -> object:
        self.stimulus_status = np.zeros((self.onset_frames[-1]-self.onset_frames[0])+int((self.seconds_before+self.stimulus_durations[-1]+self.seconds_after)*self.fps)) + 0.01 # 0.01 ~ in between stimuli
        self.stimulus_status[:self.seconds_before*self.fps] = np.arange(-self.seconds_before*self.fps-1, -1)/self.fps # pre-stimulus countdown in seconds
        for onset_frame, stimulus_duration in zip(self.onset_frames, self.stimulus_durations):
            self.stimulus_status[int(self.seconds_before*self.fps+onset_frame-self.onset_frames[0]):int((self.seconds_before+stimulus_duration)*self.fps)+onset_frame-self.onset_frames[0]]=0 # 0 ~ stimulus is ON
        self.stimulus_status[-int(self.seconds_after*self.fps):]=np.arange(1, self.seconds_after*self.fps+1)/self.fps  # post-stimulus countup in seconds

    def release_video_objects(self):
        self.source_video.release()
        self.trial_video.release()
        cv2.destroyAllWindows()
