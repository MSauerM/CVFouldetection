import cv2 as cv

class VideoWriter:

    _video_name = 'CVFouldetection.mp4'

    def __init__(self, video_name: str):
        self._video_name = video_name

    def writeVideo(self, frames, framewidth, frameheight, fps):
        # frame list oder Video processor übergeben
        video = cv.VideoWriter(self._video_name, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, (framewidth, frameheight))
        for frame in frames:
            video.write(frame)
        video.release()
        return video
