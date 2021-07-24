import numpy as np
import matplotlib.pyplot as plt

def get_color_based_on_speed(speed:float, object_to_color: str, stim_status: float=0, stim_type: str='audio') -> tuple:
    colormap, speed_thresholds = get_color_parameters(stim_type, stim_status, object_to_color)
    idx = np.where( (speed - speed_thresholds)>0 )[0][-1]
    color = ((speed_thresholds[idx+1] - speed) * colormap[idx] + (speed - speed_thresholds[idx]) * colormap[idx+1]) / (speed_thresholds[idx+1] - speed_thresholds[idx])
    if object_to_color == 'plot': color = np.append(color[::-1]/256, .7) # BGR to RGB and 0-256 to 0-1 range
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

def get_colormap(object_to_color = 'tracking video', epoch='stimulus'):
    colormap = [(0, 0, 255),(255, 0, 255),(120, 120, 255),(0, 255, 255),(0, 255, 150),(0, 150, 0),(255, 255, 0),(120,120,120),(255, 50, 0),(255, 50, 80),(255, 50, 150),(150, 0, 150),(30, 0, 180)]
    if object_to_color=='plot':
        colormap = plt.get_cmap('viridis')(np.linspace(0,.95,16))
        if epoch=='stimulus':   colormap[:,3] = np.linspace(.4, .8, 16)
        if epoch=='post-laser': colormap[:,3] = np.linspace(.3, .6, 16)
        colormap = colormap[np.array([6,11,0,5,10,15,4,9,14,3,8,13,2,7,12,1]), :]
    return colormap

def generate_list_of_colors(color_by: str='speed', stim_type: str='audio', epoch: str='stimulus', speeds: np.ndarray=None)->list:
    if color_by=='speed':
        colors = []
        for speed in speeds:
            color = get_color_based_on_speed(speed=speed, object_to_color='plot', stim_status=-1, stim_type=stim_type)
            colors.append(color)
    if color_by=='time':
        colormap = plt.get_cmap('viridis_r')
        if epoch=='stimulus': 
            colors = colormap(np.linspace(0.03,.75,len(speeds)))
            colors[:,3] = np.linspace(.4,1,len(speeds))[::-1]
        if epoch=='post-laser': 
            colors = colormap(np.linspace(.75,.75,len(speeds)))
            colors[:,3] = .2
    return colors