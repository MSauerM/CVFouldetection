import appconfig
from BasicFramework.FileWriter import FileWriter
from BasicFramework.VideoPreProcessor import VideoPreProcessor
from BasicFramework.VideoWriter import VideoWriter
from Fouldetection.Filter.BallFilter import BallFilter
from Fouldetection.Filter.GrassFilter import GrassFilter
from Fouldetection.Filter.OpticalFlowFilter import OpticalFlowFilter
from Fouldetection.Filter.PlayerFilter import PlayerFilter

from cv2 import cv2 as cv

from Fouldetection.Aggregators.FoulFrameAggregator import FoulFrameAggregator
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
        self.evaluated_contact_events = foulRecognizer.analyze(contact_events)

        foulFrameAggregator = FoulFrameAggregator()
        self.frame_list = foulFrameAggregator.aggregate(self.evaluated_contact_events, frames=self.preProcessor.frame_list)

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



       # test = str(self)
        fileWriter = FileWriter("Fouldetector_txt_out")
        fileWriter.set_output_directory("./output_info/")
        fileWriter.writeFile(self)
        print("End processing")

    def createVideo(self, filename = "FoulDetector_out"):
        videoWriter = VideoWriter(filename)
        videoWriter.set_output_directory("./output_videos/")
        dimensions = self.frame_list[0].getDimensions()
        frame_height = dimensions[0]
        frame_width = dimensions[1]
        videoWriter.writeVideo(self.frame_list, frame_width, frame_height, 25)
        return videoWriter.get_full_path()

   # def createVideo(self, filename):
   #     videoWriter = VideoWriter(filename)
   #     videoWriter.writeVideo(frames=self.frame_list)
        
    def interruptProcessing(self):
        cv.destroyAllWindows()
        self.isInterrupted = True

    def __str__(self):
        return """Overall Information:
        Execution start:{exec_start}
        Amount of Frames: {frame_count}
        
        ###############################
        Fouldetector specifics:
        
        Identified Team colors: {team_colors}
        Amount of relevant contact boxes: {amount_relevant_contact_boxes}
        Amount of aggregated sequences: {amount_aggregated_sequences}
        Amount of recognized fouls: {amount_recognized_fouls}
        
        Sequence information: 
        {sequences_info}
        
        Processing time for fouldetection: {fouldetection_processing_time} s
        
        ###############################
        Overall performance:
        
        Preprocessing time: {preprocessing_time} s
        Overall time: {overall_time} s
        
        ###############################
        
        App configuration:
        {app_config}
        
        """.format(exec_start= "nichts",
                   frame_count = 0,
                   team_colors = None,
                   amount_relevant_contact_boxes = 0,
                   amount_aggregated_sequences = 0,
                   amount_recognized_fouls = 0, #len([event for events in self.evaluated_contact_events if e])
                   sequences_info= None,
                   fouldetection_processing_time = None,
                   preprocessing_time= None,
                   overall_time = None,
                   app_config = appconfig.get_config_string())
        #return "Overall Information: \n" \
        #       "Execution start: \n" \
        #       "sfds\n" \
        #       "sdfs\n" \
        #       "\n" \
        #       "sdfs\n"\
        #    .format()
