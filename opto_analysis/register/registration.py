from opto_analysis.process.session import Session
from settings.processing_settings import processing_settings
import cv2
from typing import Tuple
import numpy as np

def get_registration_transform(session: Session, video: object, video_object: object) -> object:
    if processing_settings.skip_registration:
        return None
    else:
        rendered_arena, registration_click_targets =     generate_rendered_arena(session, processing_settings.size)
        rendered_arena_with_click_targets =              add_click_targets(rendered_arena.copy(), registration_click_targets)
        actual_arena =                                   generate_actual_arena(video_object)
        fisheye_correction_map =                         load_fisheye_correction_map(video)
        actual_arena =                                   correct_and_register_frame(actual_arena[:, :, 0], video, fisheye_correction_map)
        actual_clicked_points =                          initialize_registration_transform(actual_arena, rendered_arena_with_click_targets, registration_click_targets)
        registration_transform =                         refine_registration_transform(actual_arena, rendered_arena, registration_click_targets, actual_clicked_points)
        return registration_transform

def initialize_registration_transform(actual_arena: object, rendered_arena: object, registration_click_targets: object):
    print("\n--REGISTRATION--\nClick the points in the actual arena corresponding to the numbered dots on the rendered arena -- in order!")
    cv2.namedWindow('rendered arena')
    cv2.imshow('rendered arena', rendered_arena)
    cv2.startWindowThread()
    cv2.namedWindow('actual arena')
    actual_arena_data = [actual_arena, []]
    cv2.setMouseCallback('actual arena', click_click_targets, actual_arena_data)
    while True:
        cv2.imshow('actual arena',actual_arena)
        actual_clicked_points = actual_arena_data[1]
        if len(actual_clicked_points) == len(registration_click_targets): break # once all points are clicked
        if cv2.waitKey(10) & 0xFF == ord('q'): break
    cv2.destroyAllWindows()
    return actual_clicked_points

def refine_registration_transform(actual_arena: object, rendered_arena: object, registration_click_targets: object, actual_clicked_points: list):
    print('\nIn the overlay, left click the rendered arena and then right click the corresponding location on the actual arena -> Press space bar when finished') 
    cv2.namedWindow('overlay')
    overlay_data = [np.zeros(actual_arena.shape), actual_clicked_points, registration_click_targets, None] # None ~ registration_transformation
    cv2.setMouseCallback('overlay', click_additional_click_targets, overlay_data)
    while True:
        if len(overlay_data[1]) == len(overlay_data[2]): # if there is the same number of clicked points on the actual and rendered arenas
            # overlay_data[3] = cv2.estimateAffinePartial2D(np.array(overlay_data[1]), overlay_data[2])[0] # generate registration transformation
            overlay_data[3] = cv2.estimateAffinePartial2D(np.array(overlay_data[1]), overlay_data[2], method=cv2.RANSAC, maxIters=6000, confidence=0.995, refineIters=20)[0] # generate registration transformation
            actual_arena_registered = cv2.warpAffine(actual_arena, overlay_data[3], actual_arena.shape[::-1])
            overlay_data[0] = cv2.addWeighted(actual_arena_registered, 0.7, rendered_arena, 0.3, 0) # generate overlay image
        cv2.imshow('overlay',overlay_data[0])
        if cv2.waitKey(10) & 0xFF == ord(' '): break
    cv2.destroyAllWindows()
    return overlay_data[3] # registration transformation

def correct_and_register_frame(frame: object, video: object, fisheye_correction_map: tuple) -> object:
    if fisheye_correction_map:
        frame = cv2.copyMakeBorder(frame, video.y_offset, int((fisheye_correction_map[0].shape[0] - frame.shape[0]) - video.y_offset), video.x_offset, int((fisheye_correction_map[0].shape[1] - frame.shape[1]) - video.x_offset), cv2.BORDER_CONSTANT, value=0)
        frame = cv2.remap(frame, fisheye_correction_map[0], fisheye_correction_map[1], interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        frame = frame[video.y_offset:video.height + video.y_offset, video.x_offset:video.width + video.x_offset]
    if isinstance(video.registration_transform, np.ndarray):
        frame = cv2.warpAffine(frame, video.registration_transform, frame.shape[0:2])
    return frame

def load_fisheye_correction_map(video: object) -> tuple:
    if video.fisheye_correction_file:
        fisheye_correction = np.load(video.fisheye_correction_file);
        fisheye_correction_maps = (fisheye_correction[:, :, 0:2], fisheye_correction[:, :, 2] * 0)
    else:
        fisheye_correction_maps = None

    return fisheye_correction_maps

def generate_rendered_arena(session: Session, size: int) -> Tuple[object, object]:
    rendered_arena = 255 * np.ones((processing_settings.size,processing_settings.size)).astype(np.uint8)

    if "place preference" in session.experiment:
        pass #TODO: make place preference arena
    else:
        cv2.rectangle(rendered_arena, (int(size/2 - 250), int(size/2 - 50)), (int(size/2 + 250), int(size/2 + 50)), 190, thickness=1) # rectangular piece in the center of the arena
        cv2.rectangle(rendered_arena, (int(size/2 - 50), int(size/2 + 458)), (int(size/2 + 50), int(size/2 + 360)), 210, thickness=-1) # the shelter
        cv2.circle(rendered_arena, (int(size/2), int(size/2)), 460, 0, 1, lineType = 16) # arena outline

        points_to_click_for_registration = np.array(([size/2 - 250, size/2 - 50], \
                                                     [size/2 - 250, size/2 + 50], \
                                                     [size/2 + 250, size/2 + 50], \
                                                     [size/2 + 250, size/2 - 50])).astype(int)

    return rendered_arena, points_to_click_for_registration

def generate_actual_arena(video_object: object) -> object:
    video_object.set(cv2.CAP_PROP_POS_FRAMES, 0)
    _, frame = video_object.read()
    return frame

def add_click_targets(rendered_arena: object, registration_click_targets: object) -> object:
    for i, click_target in enumerate(registration_click_targets):
        rendered_arena_with_click_targets = cv2.circle(rendered_arena, (click_target[0], click_target[1]), 3, 255, -1)
        rendered_arena_with_click_targets = cv2.circle(rendered_arena, (click_target[0], click_target[1]), 4, 0, 1)
        rendered_arena_with_click_targets = cv2.putText(rendered_arena, str(i+1), tuple(click_target), 0, 1.0, 100, thickness=2)
    return rendered_arena_with_click_targets

def click_click_targets(event,x,y, flags, actual_arena_data):
    if event == cv2.EVENT_LBUTTONDOWN:
        actual_arena_data[0] = cv2.circle(actual_arena_data[0], (x, y), 3, 255, -1)
        actual_arena_data[0] = cv2.circle(actual_arena_data[0], (x, y), 4, 0, 1)
        actual_arena_data[1].append([x,y])

def click_additional_click_targets(event,x,y, flags, overlay_data):
    if event == cv2.EVENT_LBUTTONDOWN: # click on the rendered arena within the overlay
        cv2.circle(overlay_data[0], (x, y), 3, 0, -1)
        cv2.circle(overlay_data[0], (x, y), 4, 255, 1)
        overlay_data[2] = np.concatenate((overlay_data[2], np.reshape(np.array([x, y]),(1,2))))
    elif event == cv2.EVENT_RBUTTONDOWN: # click on the actual arena within the overlay
        cv2.circle(overlay_data[0], (x, y), 3, 255, -1)
        cv2.circle(overlay_data[0], (x, y), 4, 0, 1)
        inverse_registration_transform = cv2.invertAffineTransform(overlay_data[3])
        click_in_actual_arena_coordinates = list(np.matmul(np.append(inverse_registration_transform,np.zeros((1,3)),0), [x, y, 1])[0:2].astype(int))
        overlay_data[1].append(click_in_actual_arena_coordinates)