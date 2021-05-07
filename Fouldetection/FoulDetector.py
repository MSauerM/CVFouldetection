from BasicFramework.VideoPreProcessor import VideoPreProcessor
from BasicFramework.VideoWriter import VideoWriter
from Fouldetection.BallFilter import BallFilter
from Fouldetection.GrassFilter import GrassFilter
from Fouldetection.OpticalFlowFilter import OpticalFlowFilter
from Fouldetection.PlayerFilter import PlayerFilter

"""Obergeordnete Klasse, die den State Tracker sowie die einzenen Verarbeitungsschritte kapselt """
class FoulDetector:
    stateTracker = None
    preProcessor = None
    grassFilter = None
    playerFilter = None

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
        
