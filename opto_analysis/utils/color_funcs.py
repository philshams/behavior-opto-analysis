import numpy as np

def get_color_based_on_speed(speed:float, object_to_color: str, stim_status: float=0, stim_type: str='audio') -> tuple:
    colormap, speed_thresholds = get_color_parameters(stim_type, stim_status, object_to_color)
    idx = np.where( (speed - speed_thresholds)>0 )[0][-1]
    color = ((speed_thresholds[idx+1] - speed) * colormap[idx] + (speed - speed_thresholds[idx]) * colormap[idx+1]) / (speed_thresholds[idx+1] - speed_thresholds[idx])
    if object_to_color == 'plot': color = color[::-1]/255 # BGR to RGB and 0-256 to 0-1 range
    return color
    
def get_color_parameters(stim_type: str='audio', stim_status: float=0, object_to_color: str='trail'):
    if   stim_type == 'audio': speed_thresholds = np.array([0, 20, 40, 70, 999]) #cm/s
    elif stim_type == 'laser': speed_thresholds = np.array([0, 15, 20, 30, 999]) #cm/s

    if object_to_color=='trail' or object_to_color=='plot':
        if   stim_type=='audio':                      colormap = [[50, 50,  50], [50, 50, 100], [50, 100,200], [250,250,255], [250,250,255]]
        elif stim_type=='laser' and stim_status != 0: colormap = [[25, 25,  25], [100,50,  50], [200,100, 50], [255,230,230], [255,230,230]]
        elif stim_type=='laser' and stim_status == 0: colormap = [[255,200,  0], [255,200,  0], [255,200,  0], [255,200,  0], [255,200,  0]]
    elif object_to_color == 'text':                   colormap = [[100,100,100], [100,100,175], [100,175,220], [250,250,255], [250,250,255]]

    return [np.array(x) for x in colormap], speed_thresholds

def custom_colormap(object_to_color = 'tracking video'):
    colormap = [(0, 0, 255),(255, 0, 255),(120, 120, 255),(0, 255, 255),(0, 255, 150),(0, 150, 0),(255, 255, 0),(120,120,120),(255, 50, 0),(255, 50, 80),(255, 50, 150),(150, 0, 150),(30, 0, 180)]
    if object_to_color=='plot':
        colormap = [(200, 200, 0),(255, 50, 0),(255, 50, 150),(0, 0, 255),(255, 0, 255),(120, 120, 255),(0, 255, 255),(0, 255, 150),(0, 150, 0,),(120,120,120)]
        colormap = [tuple(c/255 for c in color)[::-1] for color in colormap]
    return colormap