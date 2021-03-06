import appconfig
from BasicFramework.FileWriter import FileWriter
from BasicFramework.VideoPreProcessor import VideoPreProcessor
from BasicFramework.VideoWriter import VideoWriter
from Fouldetection.Filter.BallFilter import BallFilter
from Fouldetection.Filter.GrassFilter import GrassFilter
from Fouldetection.Filter.OpticalFlowFilter import OpticalFlowFilter
from Fouldetection.Filter.PlayerFilter import PlayerFilter

from cv2 import cv2 as cv
from datetime import datetime

from Fouldetection.Aggregators.FoulFrameAggregator import FoulFrameAggregator
from Fouldetection.MainComponents.FoulRecognizer import FoulRecognizer
from Fouldetection.MainComponents.PreAnalyzer import PreAnalyzer

from CVUtility.PerformanceTimer import PerformanceTimer


class FoulDetector:
    """
        Class, which controls the action flow of the foul detection
        ......

        Attributes
        -----------------
            preProcessor
                instance of initial VideoPreProcessor
            isInterrupted
                flag for interrupting processing
            frame_list
                list for saving the frame for final output
            foulEvents
                list of all contact events
            evaluated_contact_events
                list of all processed contact events with foul information
            execution_start
                date time for the execution start
            preAnalyzer
                instance for the execution of pre analysis
            preAnalyzer_timer
                measures time consumed for pre analysis
            foulRecognizer
                instance for the execution of foul recognition phase
            foulRecognizer_timer
                measures time consumed for foul recognition phase
            foulDetection_timer
                measures time consumed for whole foul detection
        Methods
        -----------------
            process():
                executes whole foul detection
            createVideo(filename)
                writes the final frames of frame_list to a mp4 file named by given filename
                with VideoWriter instance
            interruptProcessing()
                interrupt the execution
        """
    preProcessor = None
    isInterrupted = False
    frame_list = []
    foulEvents = []


    execution_start = None
    overall_time=None

    def __init__(self, preProcessor: VideoPreProcessor = None, filename: str = None):
        self.preanalyzer_timer = PerformanceTimer()
        self.foulrecognition_timer = PerformanceTimer()
        self.fouldetection_timer = PerformanceTimer()

        if preProcessor is not None and filename is None:
            self.preProcessor = preProcessor
        if preProcessor is None and filename is not None:
            self.preProcessor = VideoPreProcessor(filename)

    def process(self):

        self.fouldetection_timer.start()

        self.execution_start = datetime.now()
        print("Start processing")
        self.preanalyzer_timer.start()
        self.preAnalyzer = PreAnalyzer()
        sequences, self.contact_events = self.preAnalyzer.analyze(self.preProcessor.frame_list)
        self.preanalyzer_timer.end()

        for index, sequence in enumerate(sequences):
            sequence.show_sequence()
            if appconfig.create_video_for_sequences is True:
                vwriter = VideoWriter("TEST " + str(index))
                vwriter.set_output_directory("./output_videos/")
                vwriter.write_video(sequence.get_frames(),
                                    appconfig.preferred_size_dynamic_fixed,
                                    appconfig.preferred_size_dynamic_fixed, 25)

        self.foulrecognition_timer.start()
        self.foulRecognizer = FoulRecognizer()
        self.evaluated_contact_events = self.foulRecognizer.analyze(self.contact_events)
        self.foulrecognition_timer.end()

        foulFrameAggregator = FoulFrameAggregator()
        self.frame_list = foulFrameAggregator.aggregate(self.evaluated_contact_events, frames=self.preProcessor.frame_list)

        self.fouldetection_timer.end()

        print("End processing")

    def createVideo(self, filename = "FoulDetector_out"):
        videoWriter = VideoWriter(filename)
        videoWriter.set_output_directory("./output_videos/")
        dimensions = self.frame_list[0].get_dimensions()
        frame_height = dimensions[0]
        frame_width = dimensions[1]
        videoWriter.write_video(self.frame_list, frame_width, frame_height, 25)
        return videoWriter.get_full_path()
        
    def interruptProcessing(self):
        cv.destroyAllWindows()
        self.isInterrupted = True

    def __str__(self):
        return """
    Overall Information:
        File Path: {file_path}
        Execution start: {exec_start}
        Amount of Frames: {frame_count}
        
        ###############################
        Fouldetector specifics:
        
        Identified Team colors: {team_colors}
        Amount of relevant contact boxes: {amount_relevant_contact_boxes}
        Amount of aggregated sequences: {amount_aggregated_sequences}
        Amount of recognized fouls: {amount_recognized_fouls}
        
        Contact event information: 
        {sequences_info}
        
        Processing time for pre analyzer: {pre_analyzer_time} s
        Processing time for foul recognition: {foul_recognition_processing_time} s
        Processing time for fouldetection: {fouldetection_processing_time} s
        
        ###############################
        Overall performance:
        
        Preprocessing time: {preprocessing_time} s
        Overall time: {overall_time} s
        
        ###############################
        
        App configuration:
        {app_config}
        
        """.format(exec_start=self.execution_start,
                   file_path=self.preProcessor.filepath,
                   frame_count=len(self.preProcessor.frame_list),
                   team_colors=self.preAnalyzer.teamColorCalibration.colors_list[:2],
                   amount_relevant_contact_boxes=self.preAnalyzer.candidate_box_amount,
                   amount_aggregated_sequences=len(self.contact_events),
                   amount_recognized_fouls=len([x for x in self.evaluated_contact_events if x.isFoul]),
                   sequences_info=str(self.evaluated_contact_events),
                   pre_analyzer_time=self.preanalyzer_timer.get_time(),
                   foul_recognition_processing_time=self.foulrecognition_timer.get_time(),
                   fouldetection_processing_time=self.fouldetection_timer.get_time(),
                   preprocessing_time=self.preProcessor.timer.get_time(),
                   overall_time=self.overall_time,
                   app_config=appconfig.get_config_string())

