from typing import List

import cv2 as cv
from datetime import datetime

from BasicFramework.Frame import Frame


class VideoWriter:
    """
        Class for writing the output to a mp4 file
        ......

        Attributes
        -----------------
            _video_name
                name of the output mp4 file
            _output_path
                specified output path for the output file
            _full_path
                complete path of the output mp4 file
        Methods
        -----------------
            set_output_directory(path)
                specifies the output path
            write_video(frames, framewidth, frameheight, fps)
                writes the given frames with framewidth, frameheight and fps information
                to an output mp4 file
            get_current_date_time_string()
                returns the current date time in %d-%m-%y_%H-%M-string format

        """
    _video_name = 'CVFouldetection.mp4'
    _output_path = None
    _full_path = None

    def __init__(self, video_name: str):
        self._video_name = video_name

    def set_output_directory(self, path: str):
        self._output_path = path

    def write_video(self, frames: List[Frame], framewidth, frameheight, fps):
        fourcc = cv.VideoWriter_fourcc(*'MP4V')
        self._full_path = self._output_path + self._video_name + " " + self.get_current_date_time_string() + ".mp4"
        video = cv.VideoWriter(self._output_path + self._video_name + " " + self.get_current_date_time_string() + ".mp4", fourcc, fps, (framewidth, frameheight))
        for frame in frames:
            video.write(frame.get_pixels())
        video.release()
        return video

    def get_current_date_time_string(self):
        currentDateTime = datetime.now()
        return currentDateTime.strftime("%d-%m-%y_%H-%M")

    def get_full_path(self):
        return self._full_path
