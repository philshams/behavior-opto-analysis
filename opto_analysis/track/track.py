import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
import os
import glob
import yaml
import pandas as pd
import numpy as np
import scipy.ndimage
import dill as pickle

class Track():
    def __init__(self, settings):
        self.settings = settings

    def run_deeplabcut_tracking(self, session):
        dlc_already_run = bool(glob.glob(os.path.join(session.file_path, "*DeepCut*")))
        if dlc_already_run and not self.settings.redo_dlc_tracking: 
            print("DeepLabCut tracking already saved for session:              {}".format(session.name))
        else:
            from deeplabcut.pose_estimation_tensorflow import analyze_videos
            analyze_videos(self.settings.dlc_settings_file, session.video.video_file)

    def process_tracking_data(self, session):
        already_filtered_and_registered = os.path.isfile(session.video.tracking_data_file)
        if already_filtered_and_registered and not self.settings.redo_processing_step: 
            print("Tracking data already filtered and registered for session:  {}".format(session.name))
        elif isinstance(session.video.registration_transform, type(None)):
            print("Registration not found. Tracking not processed for session: {}".format(session.name))
        else:
            print("Processing tracking data for session:                       {}".format(session.name))
            self.tracking_data = {}
            self.extract_data_from_dlc_file(session)
            self.create_array_with_dlc_tracking_data(session)
            self.replace_low_confidence_points_with_nan()
            self.interpolate_nan_values()
            self.apply_median_filter(filter_length=7)
            self.replace_points_far_from_median_bodypart_with_nan()
            self.interpolate_nan_values()
            self.fisheye_correct_tracking_data(session)
            self.register_tracking_data(session)
            self.plot_filtered_and_registered_tracking()
            self.compute_avg_bodypart_locations()
            self.compute_angles()
            self.compute_speed(session)
            self.compute_speed(session, session.video.shelter_location, 'speed rel. to shelter')
            self.save_tracking_data(session)
        print(" -----------------")

    # ------------------------------------------------------------------

    def extract_data_from_dlc_file(self, session):
        dlc_tracking_file = glob.glob(os.path.join(session.file_path, "*.h5"))[0]
        self.dlc_output = pd.read_hdf(dlc_tracking_file)
        with open(self.settings.dlc_settings_file) as file: dlc_settings = yaml.load(file)
        self.tracking_data['bodyparts'] = dlc_settings['bodyparts']
        self.dlc_network_name = dlc_tracking_file[dlc_tracking_file.find('DeepCut_resnet'):-3]

    def create_array_with_dlc_tracking_data(self, session):
        self.tracking_data_array = np.zeros((session.video.num_frames, len(self.tracking_data['bodyparts']), 3))
        for i, body_part in enumerate(self.tracking_data['bodyparts']):
            for j, axis in enumerate(['x', 'y']):
                self.tracking_data_array[:, i, j] = self.dlc_output[self.dlc_network_name][body_part][axis].values
            self.tracking_data_array[:, i, 2] = self.dlc_output[self.dlc_network_name][body_part]['likelihood'].values

    def replace_low_confidence_points_with_nan(self):
        low_confidence_points = self.tracking_data_array[:, :, 2] < self.settings.min_confidence_in_tracking
        self.tracking_data_array[low_confidence_points, :2] = np.nan 
        
    def interpolate_nan_values(self):
        for i, _ in enumerate(self.tracking_data['bodyparts']):
            self.tracking_data_array[:, i, :2] = np.array(pd.DataFrame(self.tracking_data_array[:, i, :2]).interpolate().fillna(method='bfill').fillna(method='ffill'))

    def apply_median_filter(self, filter_length=7):
        self.tracking_data_array[:, :, :2] = scipy.ndimage.median_filter(self.tracking_data_array[:, :, :2], size=(filter_length, 1, 1), mode='nearest')

    def replace_points_far_from_median_bodypart_with_nan(self):
        median_position_across_bodyparts = np.nanmedian(self.tracking_data_array[:, :, :2], axis=1) 
        distance_from_median_position = ((self.tracking_data_array[:, :, 0] - median_position_across_bodyparts[:, 0:1])**2 + \
                                         (self.tracking_data_array[:, :, 1] - median_position_across_bodyparts[:, 1:2])**2)**.5
        self.tracking_data_array[distance_from_median_position>self.settings.max_deviation_from_rest_of_points, :2] = np.nan

    def fisheye_correct_tracking_data(self, session):
        if self.settings.inverse_fisheye_correction_file:
            inverse_fisheye_map = np.load(self.settings.inverse_fisheye_correction_file)
            self.fisheye_corrected_tracking_data_array = \
                    inverse_fisheye_map[self.tracking_data_array[:,:,1].astype(np.uint16) + session.video.y_offset,     \
                                        self.tracking_data_array[:,:,0].astype(np.uint16) + session.video.x_offset, :2] \
                                            - np.array([session.video.x_offset, session.video.y_offset])
        else: 
            self.fisheye_corrected_tracking_data_array = self.tracking_data_array[:,:,:2]

    def register_tracking_data(self, session):
        for i, bodypart in enumerate(self.tracking_data['bodyparts']):
            self.tracking_data[bodypart] = np.matmul(np.append(session.video.registration_transform, np.zeros((1, 3)), 0),
                                                     np.concatenate((self.fisheye_corrected_tracking_data_array[:, i, 0:1].T,
                                                                     self.fisheye_corrected_tracking_data_array[:, i, 1:2].T,
                                                                     np.ones((1, session.video.num_frames))), 0))[:2, :].T
            assert not np.sum(self.tracking_data[bodypart] < 0), "Negative positions found after registration"

    def plot_filtered_and_registered_tracking(self):
        if self.settings.display_tracking_output:
            for axis in [0,1]:
                plt.figure()
                for bodypart in self.tracking_data['bodyparts']:
                    plt.plot(self.tracking_data[bodypart][10000:20000, axis])
                plt.legend(self.tracking_data['bodyparts'])
            plt.show()

    def compute_avg_bodypart_locations(self):
        #! This region mapping must be redone if different body parts are used during DeepLabCut tracking
        for region_mapping in [   ['avg_loc',        self.tracking_data['bodyparts']], 
                                  ['snout_loc',      ['nose', 'L eye', 'R eye']],
                                  ['neck_loc',       ['L ear', 'neck', 'R ear']],
                                  ['upper_body_loc', ['L shoulder', 'upper back', 'R shoulder']],
                                  ['lower_body_loc', ['L hind limb', 'Lower back', 'R hind limb', 'derriere']],
                                  ['head_loc',       ['snout_loc', 'neck_loc']],
                                  ['body_loc',       ['upper_body_loc', 'lower_body_loc']]  ]:
            body_region_name = region_mapping[0]
            list_of_constituent_bodyparts = region_mapping[1]
            self.tracking_data[body_region_name] = np.mean(np.array([self.tracking_data[bodypart] for bodypart in list_of_constituent_bodyparts]), axis=0)

    def compute_angles(self):
        for direction_to_compute, front_bodypart, back_bodypart in zip(['body_dir','neck_dir', 'head_dir'],
                                                                       ['upper_body_loc', 'head_loc', 'snout_loc'],
                                                                       ['body_loc', 'upper_body_loc', 'neck_loc']):
            self.tracking_data[direction_to_compute] = np.angle((self.tracking_data[front_bodypart][:, 0] - self.tracking_data[back_bodypart][:, 0]) + \
                                                               (-self.tracking_data[front_bodypart][:, 1] + self.tracking_data[back_bodypart][:, 1]) * 1j, deg=True)

    def compute_speed(self, session, reference_location=None, speed_name='speed'):
        if not reference_location:
            speed_x_and_y_pixel_per_frame = np.diff(self.tracking_data['avg_loc'], axis=0) 
            speed_pixel_per_frame = (speed_x_and_y_pixel_per_frame[:, 0]**2 + speed_x_and_y_pixel_per_frame[:, 1]**2)**.5
        else:
            distance_from_reference_location = ((self.tracking_data['avg_loc'][:,0] - reference_location[0])**2 + \
                                                (self.tracking_data['avg_loc'][:,1] - reference_location[1])**2)**.5
            speed_pixel_per_frame = -np.diff(distance_from_reference_location)
        speed_cm_per_sec = speed_pixel_per_frame * session.video.fps / session.video.pixels_per_cm
        smoothed_speed_cm_per_sec = gaussian_filter1d(speed_cm_per_sec, sigma=session.video.fps/10)
        self.tracking_data[speed_name] = smoothed_speed_cm_per_sec
       

    def save_tracking_data(self, session):
        with open(session.video.tracking_data_file, "wb") as dill_file: pickle.dump(self.tracking_data, dill_file)
