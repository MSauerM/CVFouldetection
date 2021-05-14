from typing import List

from BasicFramework.Frame import Frame
from Fouldetection.Filter.BallFilter import BallFilter
from Fouldetection.Filter.CourtBoundsFilter import CourtBoundsFilter
from Fouldetection.Filter.GrassFilter import GrassFilter
from Fouldetection.Filter.PlayerFilter import PlayerFilter



class PreAnalyzer:

    isInterrupted = False

    def __init__(self):
        print("Init PreAnalyzer")


    def analyze(self, frame_list:List[Frame]):
        print("Start processing")
        grassFilter = GrassFilter()
        ballFilter = BallFilter()
        playerFilter = PlayerFilter()
        #opticalFlowFilter = OpticalFlowFilter(self.preProcessor.frame_list)
        courtBoundsFilter = CourtBoundsFilter()
        # opticalFlowFilter.filter()

        # detect Players and Ball / extract basic game information
        for frame in frame_list:
            if self.isInterrupted:
                break
            courtBoundsFilter.filter(frame)
            grassFilteredFrame = grassFilter.filter(frame)
            candidateBoundingBoxes = playerFilter.filter(frame, grassFilteredFrame)
            # ballFilter.filter(frame)
        # self.frame_list.append()

        return None # Sequences of possible foul plays