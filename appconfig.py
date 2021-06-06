from enum import Enum

class CroppingStrategy(Enum):
    STATIONARY = 1
    DYNAMIC_FIXED = 2
    DYNAMIC_VARIED = 3

use_multithreading = False
team_color_calib_every_frame = False
max_frame_amount = 2000
show_debug_windows = True
cropping_strategy = CroppingStrategy.DYNAMIC_FIXED #STATIONARY #DYNAMIC_FIXED # DYNAMIC_VARIED
preferred_size_dynamic_fixed = 448 # None or int for quadratic size

create_video_for_sequences = False