from typing import List

from BasicFramework.Frame import Frame
from Fouldetection.Filter.BallFilter import BallFilter
from Fouldetection.Filter.GrassFilter import GrassFilter
from Fouldetection.Filter.PlayerFilter import PlayerFilter


class PreAnalyzer:

    def __init__(self):
        print("Init PreAnalyzer")


    def analyze(self, frame_list:List[Frame]):
        print("Start processing")
        grassFilter = GrassFilter()
        ballFilter = BallFilter()
        playerFilter = PlayerFilter()
        #opticalFlowFilter = OpticalFlowFilter(self.preProcessor.frame_list)

        # opticalFlowFilter.filter()

        # detect Players and Ball / extract basic game information
        for frame in self.preProcessor.frame_list:
            if self.isInterrupted:
                break

            grassFilteredFrame = grassFilter.filter(frame)
            playerFilter.filter(frame, grassFilteredFrame)
            # ballFilter.filter(frame)
        # self.frame_list.append()

        return None # BoundingBox List