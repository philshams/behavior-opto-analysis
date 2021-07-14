from opto_analysis.process.session import Session
from settings.processing_settings import processing_settings
import cv2
import numpy as np


def correct_and_register_frame(frame: object, video: object, fisheye_correction_map: tuple) -> object:
    if fisheye_correction_map:
        frame = cv2.copyMakeBorder(frame, video.y_offset, int((fisheye_correction_map[0].shape[0] - frame.shape[0]) - video.y_offset), video.x_offset, int((fisheye_correction_map[0].shape[1] - frame.shape[1]) - video.x_offset), cv2.BORDER_CONSTANT, value=0)
        frame = cv2.remap(frame, fisheye_correction_map[0], fisheye_correction_map[1], interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        frame = frame[video.y_offset:video.height + video.y_offset, video.x_offset:video.width + video.x_offset]
    if isinstance(video.registration_transform, np.ndarray):
        frame = cv2.warpAffine(frame, video.transform, frame.shape[0:2])
    return frame

def load_fisheye_correction_map(video: object):
    if video.fisheye_correction_file:
        fisheye_correction = np.load(video.fisheye_correction_file);
        fisheye_correction_map = (fisheye_correction[:, :, 0:2], fisheye_correction[:, :, 2] * 0)
    else:
        fisheye_correction_map = None
    return fisheye_correction_map
    
class Registration():
    def __init__(self, session: Session, video: object, video_object: object) -> object:
        self.generate_rendered_arena(session, processing_settings.size)
        self.add_click_targets()
        self.generate_actual_arena(video_object)
        self.fisheye_correction_map = load_fisheye_correction_map(video)
        self.actual_arena = correct_and_register_frame(self.actual_arena[:, :, 0], video, self.fisheye_correction_map)
        self.initialize_transform()
        self.refine_transform()

    def generate_rendered_arena(self, session: Session, size: int):
        self.rendered_arena = 255 * np.ones((size, size)).astype(np.uint8)

        if "place preference" in session.experiment:
            pass #TODO: make place preference arena
        else:
            cv2.rectangle(self.rendered_arena, (int(size/2 - 250), int(size/2 - 50)), (int(size/2 + 250), int(size/2 + 50)), 190, thickness=1) # rectangular piece in the center of the arena
            cv2.rectangle(self.rendered_arena, (int(size/2 - 50), int(size/2 + 458)), (int(size/2 + 50), int(size/2 + 360)), 210, thickness=-1) # the shelter
            cv2.circle(self.rendered_arena, (int(size/2), int(size/2)), 460, 0, 1, lineType = 16) # arena outline

            self.click_targets = np.array(([size/2 - 250, size/2 - 50], [size/2 - 250, size/2 + 50], [size/2 + 250, size/2 + 50], [size/2 + 250, size/2 - 50])).astype(int)

    def add_click_targets(self):
        for i, click_target in enumerate(self.click_targets):
            self.rendered_arena_with_click_targets = cv2.circle(self.rendered_arena, (click_target[0], click_target[1]), 3, 255, -1)
            self.rendered_arena_with_click_targets = cv2.circle(self.rendered_arena, (click_target[0], click_target[1]), 4, 0, 1)
            self.rendered_arena_with_click_targets = cv2.putText(self.rendered_arena, str(i+1), tuple(click_target), 0, 1.0, 100, thickness=2)

    def generate_actual_arena(self, video_object: object):
        video_object.set(cv2.CAP_PROP_POS_FRAMES, 0)
        _, self.actual_arena = video_object.read()

    def initialize_transform(self):
        print("\n--REGISTRATION--\nClick the points in the actual arena corresponding to the numbered dots on the rendered arena -- in order!")
        cv2.namedWindow('rendered arena')
        cv2.imshow('rendered arena', self.rendered_arena)
        cv2.startWindowThread()
        cv2.namedWindow('actual arena')
        # actual_arena_data = [actual_arena, []]
        self.actual_clicked_points = []
        cv2.setMouseCallback('actual arena', self.click_click_targets)
        while True:
            cv2.imshow('actual arena', self.actual_arena)
            if len(self.actual_clicked_points) == len(self.click_targets): break # once all points are clicked
            if cv2.waitKey(10) & 0xFF == ord('q'): break
        cv2.destroyAllWindows()

    def refine_transform(self):
        print('\nIn the overlay, left click the rendered arena and then right click the corresponding location on the actual arena -> Press space bar when finished') 
        cv2.namedWindow('overlay')
        cv2.setMouseCallback('overlay', self.click_additional_click_targets, self)
        while True:
            if len(self.actual_clicked_points) == len(self.click_targets) and self.time_to_update:
                self.transform = cv2.estimateAffinePartial2D(np.array(self.actual_clicked_points), self.click_targets, method=cv2.RANSAC, maxIters=6000, confidence=0.995, refineIters=20)[0]
                actual_arena_registered = cv2.warpAffine(self.actual_arena, self.transform, self.actual_arena.shape[::-1])
                self.overlay_of_arenas = cv2.addWeighted(actual_arena_registered, 0.7, self.rendered_arena, 0.3, 0)
                self.time_to_update = False
            cv2.imshow('overlay', self.overlay_of_arenas)
            if cv2.waitKey(10) & 0xFF == ord(' '): break
        cv2.destroyAllWindows()

    def click_click_targets(self, event,x,y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.actual_arena = cv2.circle(self.actual_arena, (x, y), 3, 255, -1)
            self.actual_arena = cv2.circle(self.actual_arena, (x, y), 4, 0, 1)
            # actual_arena_data[1].append([x,y])
            self.actual_clicked_points.append([x,y])
            self.time_to_update = True

    def click_additional_click_targets(self, event,x,y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN: # click on the rendered arena within the overlay
            cv2.circle(self.overlay_of_arenas, (x, y), 3, 0, -1)
            cv2.circle(self.overlay_of_arenas, (x, y), 4, 255, 1)
            self.click_targets = np.concatenate((self.click_targets, np.reshape(np.array([x, y]),(1,2))))
        elif event == cv2.EVENT_RBUTTONDOWN: # click on the actual arena within the overlay
            cv2.circle(self.overlay_of_arenas, (x, y), 3, 255, -1)
            cv2.circle(self.overlay_of_arenas, (x, y), 4, 0, 1)
            inverse_transform = cv2.invertAffineTransform(self.transform)
            click_in_actual_arena_coordinates = list(np.matmul(np.append(inverse_transform,np.zeros((1,3)),0), [x, y, 1])[0:2].astype(int))
            self.actual_clicked_points.append(click_in_actual_arena_coordinates)
        self.time_to_update = True