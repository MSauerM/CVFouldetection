from BasicFramework.VideoPreProcessor import VideoPreProcessor
from BasicFramework.VideoWriter import VideoWriter
from Fouldetection.GrassFilter import GrassFilter
from Fouldetection.PlayerFilter import PlayerFilter

"""Obergeordnete Klasse, die den State Tracker sowie die einzenen Verarbeitungsschritte kapselt """
class FoulDetector:
    stateTracker = None
    preProcessor = None
    grassFilter = None
    playerFilter = None

    frame_list = []
    foulEvents = []

    def __init__(self, preProcessor: VideoPreProcessor):
        self.preProcessor = preProcessor

    def process(self):
        print("Start processing")
        grassFilter = GrassFilter()
        # ballFilter = BallFilter()
        playerFilter = PlayerFilter()

        for frame in self.preProcessor.frame_list:
            grassFilteredFrame = grassFilter.filter(frame)
            playerFilter.filter(frame, grassFilteredFrame)

            self.frame_list.append()
        # filteredGrass = grassFilter.filter(preProcessor.framelist);
        # filteredBall = ballFilter.filter(filteredGrass);
        # filteredPlayer = playerFilter.filter(filteredGrass);

        print("End processing")

    def createVideo(self):
        videoWriter = VideoWriter("FoulDetector")
        videoWriter.writeVideo(frames=self.frame_list)
        
