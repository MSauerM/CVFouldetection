from enum import Enum

class CroppingStrategy(Enum):
    STATIONARY = 1
    DYNAMIC_FIXED = 2
    DYNAMIC_VARIED = 3

use_multithreading = False
team_color_calib_every_frame = False
max_frame_amount = 2000
show_debug_windows = False
cropping_strategy = CroppingStrategy.DYNAMIC_FIXED #STATIONARY #DYNAMIC_FIXED # DYNAMIC_VARIED
preferred_size_dynamic_fixed = 448#224 # 448 # None or int for quadratic size

create_video_for_sequences = False

####### CNN networks
use_action_recognition = True
use_human_pose_estimation = False

def get_config_string():
    return """ 
     use_multithreading: {use_multithreading}
     team_color_calib_every_frame: {team_color_calib_every_frame}
     max_frame_amount: {max_frame_amount}
     show_debug_windows: {show_debug_windows}
     cropping_strategy: {cropping_strategy}
     preferred_size_dynamic_fixed: {preferred_size_dynamic_fixed}
     create_video_for_sequences: {create_video_for_sequences}
     use_action_recognition: {use_action_recognition}
     use_human_pose_estimation: {use_human_pose_estimation}
    
    """.format(use_multithreading= use_multithreading,
               team_color_calib_every_frame= team_color_calib_every_frame,
               max_frame_amount = max_frame_amount,
               show_debug_windows= show_debug_windows,
               cropping_strategy = cropping_strategy,
               preferred_size_dynamic_fixed = preferred_size_dynamic_fixed,
               create_video_for_sequences = create_video_for_sequences,
               use_action_recognition = use_action_recognition,
               use_human_pose_estimation = use_human_pose_estimation
               )