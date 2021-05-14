from BasicFramework.VideoPreProcessor import VideoPreProcessor
from BasicFramework.VideoWriter import VideoWriter
from Fouldetection.Filter.BallFilter import BallFilter
from Fouldetection.Filter.GrassFilter import GrassFilter
from Fouldetection.Filter.OpticalFlowFilter import OpticalFlowFilter
from Fouldetection.Filter.PlayerFilter import PlayerFilter

from cv2 import cv2 as cv

"""Obergeordnete Klasse, die den State Tracker sowie die einzenen Verarbeitungsschritte kapselt """
class FoulDetector:
    stateTracker = None
    preProcessor = None
    grassFilter = None
    playerFilter = None

    isInterrupted = False

    frame_list = []
    foulEvents = []
    # boundingBoxInformation

    def __init__(self, preProcessor: VideoPreProcessor):
        self.preProcessor = preProcessor

    def process(self):
        print("Start processing")
        grassFilter = GrassFilter()
        ballFilter = BallFilter()
        playerFilter = PlayerFilter()
        opticalFlowFilter = OpticalFlowFilter(self.preProcessor.frame_list)


        #opticalFlowFilter.filter()

        # detect Players and Ball / extract basic game information
        for frame in self.preProcessor.frame_list:
            if self.isInterrupted:
                break

            grassFilteredFrame = grassFilter.filter(frame)
            playerFilter.filter(frame, grassFilteredFrame)
            #ballFilter.filter(frame)
           # self.frame_list.append()


            # retrieve boundingBox Information on every single frame


        # Aggregate frames to Contact Events





        print("End processing")

    def createVideo(self):
        videoWriter = VideoWriter("FoulDetector")
        videoWriter.writeVideo(frames=self.frame_list)

    def createVideo(self, filename):
        videoWriter = VideoWriter(filename)
        videoWriter.writeVideo(frames=self.frame_list)
        
    def interruptProcessing(self):
        cv.destroyAllWindows()
        self.isInterrupted = True
