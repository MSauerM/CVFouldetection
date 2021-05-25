from typing import List

from BasicFramework.Frame import Frame
from Fouldetection.ContactBoxChecker import ContactBoxChecker
from Fouldetection.Filter.BallFilter import BallFilter
from Fouldetection.Filter.CourtBoundsFilter import CourtBoundsFilter
from Fouldetection.Filter.GrassFilter import GrassFilter
from Fouldetection.Filter.PlayerFilter import PlayerFilter
from Fouldetection.TeamColorCalibration import TeamColorCalibration


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
        teamColorCalibration = TeamColorCalibration()
        # opticalFlowFilter.filter()
        contactBoxChecker = ContactBoxChecker(teamColorCalibration)

        contact_boxes = []

        # detect Players and Ball / extract basic game information
        for frame in frame_list:
            if self.isInterrupted:
                break
            #courtBoundsFilter.filter(frame)

            grassFilteredFrame, fieldMask = grassFilter.filter(frame)
            ballFilter.filter(frame, (grassFilteredFrame, fieldMask))
            candidateBoundingBoxes = playerFilter.filter(frame, grassFilteredFrame)
            if not teamColorCalibration.isCalibrated:
                teamColorCalibration.calibrate(frame.getPixels(), grassFilteredFrame)


            for candidate in candidateBoundingBoxes:
                if contactBoxChecker.check_for_contact(frame.getPixels(), grassFilteredFrame, candidate):
                    contact_boxes.append(candidate)

            # analyze candidate Bounding Boxes for real players
            # cut out the candidate Bounding Boxes out of the real image

            # make a color histogram out of it

            # ballFilter.filter(frame)
        # self.frame_list.append()
        print(contact_boxes)
        sequences = []


        return sequences # Sequences of possible foul plays