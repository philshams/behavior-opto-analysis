from opto_analysis.run import track_data
from settings.tracking_settings import tracking_settings
from pathlib import Path
import os
import glob
import yaml
import pandas as pd
import numpy as np
import scipy.ndimage

class Track():

    def run_deeplabcut_tracking(self, session):
        dlc_already_run = bool(glob.glob(os.path.join(session.file_path, "*DeepCut*")))
        if dlc_already_run and not tracking_settings.redo_dlc_tracking: 
            print("DeepLabCut tracking already saved for session {}".format(session.name))
        else:
            from deeplabcut.pose_estimation_tensorflow import analyze_videos
            analyze_videos(tracking_settings.dlc_settings_file, session.video.video_file)

    def process_tracking_data(self, session):
        already_filtered_and_registered = os.path.isfile(os.path.join(session.file_path, "tracking_data"))
        if already_filtered_and_registered and not tracking_settings.redo_processing_step: 
            print("Tracking data already filtered and registered for session: {}".format(session.name))
        elif isinstance(session.video.registration_transform, type(None)):
            print("No registration transform found -- tracking data not processed")
        else:
            self.tracking_data = {}
            self.extract_data_from_dlc_file(session)
            self.create_array_with_dlc_tracking_data(session)
            self.replace_low_confidence_points_with_nan()
            self.replace_points_far_from_median_bodypart_with_nan()
            self.interpolate_nan_values()
            self.apply_median_filter(filter_length=7)
            self.register_tracking_data(session)
            self.display_tracking_output()
            self.compute_tracking_metrics()
            self.save_tracking_data()
        print(" -----------------")

    # --------------------------------------------------------------------------------------------------

    def extract_data_from_dlc_file(self, session):
        dlc_tracking_file = glob.glob(os.path.join(session.file_path, "*.h5"))[0]
        self.dlc_tracking_data = pd.read_hdf(dlc_tracking_file)
        with open(tracking_settings.dlc_settings_file) as file: dlc_settings = yaml.load(file)
        self.tracking_data['bodyparts'] = dlc_settings['bodyparts']
        self.dlc_network_name = dlc_tracking_file[dlc_tracking_file.find('DeepCut_resnet'):-3]

    def create_array_with_dlc_tracking_data(self, session):
        self.dlc_tracking_data_array = np.zeros((session.video.num_frames, len(self.tracking_data['bodyparts']), 3))
        for i, body_part in enumerate(self.tracking_data['bodyparts']):
            for j, axis in enumerate(['x', 'y']):
                self.dlc_tracking_data_array[:, i, j] = self.dlc_tracking_data[self.dlc_network_name][body_part][axis].values
            self.dlc_tracking_data_array[:, i, 2] = self.dlc_tracking_data[self.dlc_network_name][body_part]['likelihood'].values

    def replace_low_confidence_points_with_nan(self):
        low_confidence_points = self.dlc_tracking_data_array[:, :, 2] < tracking_settings.min_confidence_in_tracking
        self.dlc_tracking_data_array[low_confidence_points, :2] = np.nan 
        
    def replace_points_far_from_median_bodypart_with_nan(self):
        median_position_across_bodyparts = np.nanmedian(self.dlc_tracking_data_array[:, :, :2], axis=1) 
        distance_from_median_position = ((self.dlc_tracking_data_array[:, :, 0] - median_position_across_bodyparts[:, 0:1])**2 + \
                                         (self.dlc_tracking_data_array[:, :, 1] - median_position_across_bodyparts[:, 1:2])**2)**.5
        self.dlc_tracking_data_array[distance_from_median_position>tracking_settings.max_deviation_from_rest_of_points, :2] = np.nan

    def interpolate_nan_values(self):
        for i, _ in enumerate(self.tracking_data['bodyparts']):
            self.dlc_tracking_data_array[:, i, :2] = np.array(pd.DataFrame(self.dlc_tracking_data_array[:, i, :2]).interpolate().fillna(method='bfill').fillna(method='ffill'))

    def apply_median_filter(self, filter_length=7):
        self.dlc_tracking_data_array[:, :, :2] = scipy.ndimage.median_filter(self.dlc_tracking_data_array[:, :, :2], size=(filter_length, 1, 1), mode='nearest')

    def register_tracking_data(self, session):
        if tracking_settings.inverse_fisheye_correction_file:
            inverse_fisheye_map = np.load(tracking_settings.inverse_fisheye_correction_file)
            self.fisheye_corrected_tracking_data = inverse_fisheye_map[self.dlc_tracking_data_array[:,:,1].astype(np.uint16) + session.video.y_offset,     \
                                                                self.dlc_tracking_data_array[:,:,0].astype(np.uint16) + session.video.x_offset, :2] \
                                                                 - np.array([session.video.x_offset, session.video.y_offset])
        else: self.fisheye_corrected_tracking_data = self.dlc_tracking_data_array[:,:,:2]

        self.registered_tracking_data = np.matmul(np.append(session.video.registration_transform, np.zeros((1, 3)), 0),
                                                  np.concatenate((self.fisheye_corrected_tracking_data,np.ones((1, len(track_data['bodyparts']), session.video.num_frames))), 0))
    #TODO: get this working - attempt single step correction and multiplication, but do it in loops if that isn't feasible

    def display_tracking_output(self):
        pass

    def compute_tracking_metrics(self):
        pass

    def save_tracking_data(self):
        pass

    # --------------------------------------------------------------------------------------------------

