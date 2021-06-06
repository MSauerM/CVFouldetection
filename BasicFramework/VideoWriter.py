from typing import List

import cv2 as cv
from datetime import datetime

from BasicFramework.Frame import Frame


class VideoWriter:

    _video_name = 'CVFouldetection.mp4'

    def __init__(self, video_name: str):
        self._video_name = video_name

    def writeVideo(self, frames: List[Frame], framewidth, frameheight, fps):
        # frame list oder Video processor übergeben
        #frames[0].shape
        video = cv.VideoWriter(self._video_name + " " + self.getCurrentDateTimeString(), cv.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, (framewidth, frameheight))
        for frame in frames:
            video.write(frame.getPixels())
        video.release()
        return video

    def getCurrentDateTimeString(self):
        currentDateTime = datetime.now()
        return currentDateTime.strftime("%d-%m-%y_%H-%M")