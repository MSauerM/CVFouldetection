import appconfig
from Fouldetection.Analyzers.ActionRecognizer import ActionRecognizer


class FoulAnalyzer:

    def __init__(self):
        print("Init FoulAnalyzer")
        if appconfig.use_action_recognition:
            self.action_recognizer = ActionRecognizer("./Fouldetection/Analyzers/i3d 27-06-21_12-02.params")

    def analyze_human_pose(self, joints: dict):
        print("Analyze Foul based on Human Pose")

    def analyze_action(self, sequence):
        print("Analyze Foul based on Action Recognition")
        probabilities = self.action_recognizer.classify(sequence)
        print(probabilities)
        return probabilities
