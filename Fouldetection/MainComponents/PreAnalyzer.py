from typing import List

import appconfig
from BasicFramework.Frame import Frame
from CVUtility.PerformanceTimer import PerformanceTimer
from Fouldetection.Analyzers.ContactBoxChecker import ContactBoxChecker
from Fouldetection.DataStructures.ContactEvent import ContactEvent
from Fouldetection.Aggregators.ContactSequenceAggregator import ContactSequenceAggregator
from Fouldetection.Filter.BallFilter import BallFilter
from Fouldetection.Filter.CourtBoundsFilter import CourtBoundsFilter
from Fouldetection.Filter.GrassFilter import GrassFilter
from Fouldetection.Filter.PlayerFilter import PlayerFilter
from Fouldetection.Analyzers.TeamColorCalibration import TeamColorCalibration
from cv2 import cv2 as cv
from CVUtility import ImageUtility as utility


class PreAnalyzer:
    """
        Class for ....
        ......

        Attributes
        -----------------



        Methods
        -----------------

        """
    isInterrupted = False
    candidate_box_amount = 0

    def __init__(self):
        print("Init PreAnalyzer")

    def analyze(self, frame_list:List[Frame]):
        print("Start processing")
        grassFilter = GrassFilter()
        playerFilter = PlayerFilter()
        self.teamColorCalibration = TeamColorCalibration()
        contactBoxChecker = ContactBoxChecker(self.teamColorCalibration)
        contactSequenceAggregator = ContactSequenceAggregator()


        contact_boxes = dict()#[]

        timer = PerformanceTimer("Frame Processing")
        timer.start()
        contactCheckTimer= PerformanceTimer("ContactBoxChecker")
        # detect Players and Ball / extract basic game information
        print("Start Processing of Frames")
        for frame in frame_list:
            if self.isInterrupted:
                break
            #################################################################
            grassFilteredFrame, fieldMask = grassFilter.filter(frame)  # 0.045 on average
            candidateBoundingBoxes, player_edges = playerFilter.filter(frame, (grassFilteredFrame, fieldMask))
            ##################################################################
            if appconfig.team_color_calib_every_frame:
                self.teamColorCalibration.calibrate(frame.get_pixels(), player_edges)
            else:
                if not self.teamColorCalibration.isCalibrated:
                    self.teamColorCalibration.calibrate(frame.get_pixels(), grassFilteredFrame)#player_edges)

            contact_boxes[frame.get_frame_index()] = []
            contactCheckTimer.start()
            combined_img = cv.bitwise_and(frame.get_pixels(), frame.get_pixels(), mask = player_edges)
            utility.showResizedImage("Test - Combined Image", combined_img, 0.4)
            for candidate in candidateBoundingBoxes:
                if contactBoxChecker.check_for_contact(combined_img, player_edges, candidate):
                    #x,y,w,h = candidate.get_bounds()
                    contact_boxes[frame.get_frame_index()].append(candidate)
                    self.candidate_box_amount += 1
            contactCheckTimer.end()
            utility.showResizedImage("Relevant Boxes - Pre Analyzer", frame.get_pixels(), 0.6)
        timer.end()
        print(timer)
        print(contact_boxes)
        sequences, bounding_box_chains = contactSequenceAggregator.aggregate(frame_list, contact_boxes)
        contact_events = []
        for i in range(0, len(sequences)):
            contact_events.append(ContactEvent(sequences[i], bounding_box_chains[i]))
        return sequences, contact_events   # Sequences of possible foul plays
