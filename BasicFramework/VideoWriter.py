from typing import List

import cv2 as cv
from datetime import datetime

from BasicFramework.Frame import Frame


class VideoWriter:

    _video_name = 'CVFouldetection.mp4'
    _output_path = None
    _full_path = None

    def __init__(self, video_name: str):
        self._video_name = video_name

    def set_output_directory(self, path: str):
        self._output_path = path

    def writeVideo(self, frames: List[Frame], framewidth, frameheight, fps):
        # frame list oder Video processor übergeben
        #frames[0].shape
        #fourcc = cv.VideoWriter_fourcc('M', 'J', 'P', 'G')
        #fourcc = cv.VideoWriter_fourcc(*'MPEG')
        fourcc = cv.VideoWriter_fourcc(*'MP4V')
        self._full_path = self._output_path + self._video_name + " " + self.getCurrentDateTimeString()+".mp4"
        video = cv.VideoWriter(self._output_path + self._video_name + " " + self.getCurrentDateTimeString()+".mp4", fourcc, fps, (framewidth, frameheight))
        for frame in frames:
            video.write(frame.getPixels())
        video.release()
        return video

    def getCurrentDateTimeString(self):
        currentDateTime = datetime.now()
        return currentDateTime.strftime("%d-%m-%y_%H-%M")

    def get_full_path(self):
        return self._full_path
