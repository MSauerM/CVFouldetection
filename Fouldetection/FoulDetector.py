import appconfig
from BasicFramework.VideoPreProcessor import VideoPreProcessor
from BasicFramework.VideoWriter import VideoWriter
from Fouldetection.Filter.BallFilter import BallFilter
from Fouldetection.Filter.GrassFilter import GrassFilter
from Fouldetection.Filter.OpticalFlowFilter import OpticalFlowFilter
from Fouldetection.Filter.PlayerFilter import PlayerFilter

from cv2 import cv2 as cv

from Fouldetection.FoulFrameAggregator import FoulFrameAggregator
from Fouldetection.MainComponents.FoulRecognizer import FoulRecognizer
from Fouldetection.MainComponents.PreAnalyzer import PreAnalyzer

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

    def __init__(self, preProcessor: VideoPreProcessor = None, filename: str = None):
        if preProcessor is not None and filename is None:
            self.preProcessor = preProcessor
        if preProcessor is None and filename is not None:
            self.preProcessor = VideoPreProcessor(filename)

    def process(self):
        print("Start processing")
        preAnalyzer = PreAnalyzer()
        sequences, contact_events = preAnalyzer.analyze(self.preProcessor.frame_list)

        for index, sequence in enumerate(sequences):
            sequence.showSequence()
            if appconfig.create_video_for_sequences is True:
                vwriter = VideoWriter("TEST " + str(index))
                vwriter.set_output_directory("./output_videos/")
                vwriter.writeVideo(sequence.getFrames(),
                                   appconfig.preferred_size_dynamic_fixed,
                                   appconfig.preferred_size_dynamic_fixed, 25)

        foulRecognizer = FoulRecognizer()
        evaluated_contact_events = foulRecognizer.analyze(contact_events)

        foulFrameAggregator = FoulFrameAggregator()
        self.frame_list = foulFrameAggregator.aggregate(evaluated_contact_events, frames=self.preProcessor.frame_list)

        #grassFilter = GrassFilter()
        #ballFilter = BallFilter()
        #playerFilter = PlayerFilter()
        #opticalFlowFilter = OpticalFlowFilter(self.preProcessor.frame_list)


        #opticalFlowFilter.filter()

        # detect Players and Ball / extract basic game information
        #for frame in self.preProcessor.frame_list:
        #    if self.isInterrupted:
        #        break

        #    grassFilteredFrame = grassFilter.filter(frame)
        #    playerFilter.filter(frame, grassFilteredFrame)
            #ballFilter.filter(frame)
           # self.frame_list.append()


            # retrieve boundingBox Information on every single frame


        # Aggregate frames to Contact Events





        print("End processing")

    def createVideo(self, filename = "FoulDetector"):
        videoWriter = VideoWriter(filename)
        dimensions = self.frame_list[0].getDimensions()
        frame_height = dimensions[0]
        frame_width = dimensions[1]
        videoWriter.writeVideo(self.frame_list, frame_width, frame_height, 25)

   # def createVideo(self, filename):
   #     videoWriter = VideoWriter(filename)
   #     videoWriter.writeVideo(frames=self.frame_list)
        
    def interruptProcessing(self):
        cv.destroyAllWindows()
        self.isInterrupted = True
