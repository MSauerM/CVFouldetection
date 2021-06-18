from typing import List

from BasicFramework.Frame import Frame
from CVUtility.PerformanceTimer import PerformanceTimer
from Fouldetection.ContactBoxChecker import ContactBoxChecker
from Fouldetection.ContactEvent import ContactEvent
from Fouldetection.ContactSequenceAggregator import ContactSequenceAggregator
from Fouldetection.Filter.BallFilter import BallFilter
from Fouldetection.Filter.CourtBoundsFilter import CourtBoundsFilter
from Fouldetection.Filter.GrassFilter import GrassFilter
from Fouldetection.Filter.PlayerFilter import PlayerFilter
from Fouldetection.TeamColorCalibration import TeamColorCalibration
from cv2 import cv2 as cv
from CVUtility import ImageUtility as utility

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
        contactSequenceAggregator = ContactSequenceAggregator()


        contact_boxes = dict()#[]

        timer = PerformanceTimer("Frame Processing")
        timer.start()
        contactCheckTimer= PerformanceTimer("ContactBoxChecker")
        frameTimer = PerformanceTimer("Per-Frame BallFilter")
        # detect Players and Ball / extract basic game information
        print("Start Processing of Frames")
        for frame in frame_list:
            if self.isInterrupted:
                break
            #courtBoundsFilter.filter(frame)
            # bottle neck of bad performance is in the following part
            #################################################################
            grassFilteredFrame, fieldMask = grassFilter.filter(frame)  # 0.045 on average

            #frameTimer.start()
            #ballFilter.filter(frame, (grassFilteredFrame, fieldMask)) # 0.34 on average  #### BALLFILTER IS THE BOTTLE-NECK
            #frameTimer.end()
            #print(frameTimer)

            candidateBoundingBoxes, player_edges = playerFilter.filter(frame, (grassFilteredFrame, fieldMask)) # 0.026 on average

            ##################################################################
            if not teamColorCalibration.isCalibrated:
                teamColorCalibration.calibrate(frame.getPixels(), player_edges)

            contact_boxes[frame.getFrameCount()] = []
            # hier Bild schon aus frame.getPixels und grassFilteredFrame zusammensetzen,
            # dies löst auch Problematik mit dem caching

            contactCheckTimer.start()
            combined_img = cv.bitwise_and(frame.getPixels(), frame.getPixels(), mask = player_edges)
            for candidate in candidateBoundingBoxes:
                #if contactBoxChecker.check_for_contact(frame.getPixels(), grassFilteredFrame, candidate):
                if contactBoxChecker.check_for_contact(combined_img, player_edges, candidate):
                    x,y,w,h = candidate.get_bounds()
                    cv.rectangle(frame.getPixels(), (x, y), (x+w, y+h), (255, 0, 255), 3)
                    contact_boxes[frame.getFrameCount()].append(candidate)
                else:
                    x, y, w, h = candidate.get_bounds()
                    cv.rectangle(frame.getPixels(), (x, y), (x + w, y + h), (0, 0, 255), 3)
            contactCheckTimer.end()
            utility.showResizedImage("Relevant Boxes - Pre Analyzer", frame.getPixels(), 0.6)
            #print(contactCheckTimer)
        timer.end()
        print(timer)
            # analyze candidate Bounding Boxes for real players
            # cut out the candidate Bounding Boxes out of the real image

            # make a color histogram out of it

            # ballFilter.filter(frame)
        # self.frame_list.append()
        print(contact_boxes)
        sequences, bounding_box_chains = contactSequenceAggregator.aggregate(frame_list, contact_boxes)
        contact_events = []
        for i in range(0, len(sequences)):
            contact_events.append(ContactEvent(sequences[i], bounding_box_chains[i]))
        return sequences, contact_events # Sequences of possible foul plays