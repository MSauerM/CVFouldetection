from typing import List

import appconfig
from Fouldetection.DataStructures.ContactEvent import ContactEvent
from Fouldetection.Analyzers.FoulAnalyzer import FoulAnalyzer
from Fouldetection.Analyzers.HumanPoseEstimator import HumanPoseEstimator


class FoulRecognizer:

    def __init__(self):
        print("FoulRecognizer")
        self.foul_analyzer = FoulAnalyzer()

    def analyze(self, contact_events: List[ContactEvent]):
        print("Checking for possible fouls")
        if appconfig.use_human_pose_estimation:
            print("Use human pose estimation for foul recognition")
            joints_dict_list = []
            human_pose_estimator = HumanPoseEstimator()
            ### Analyze loop
            for _, event in enumerate(contact_events):
                sequence = event.sequence
                joints_dict = dict()
                for index, frame in enumerate(sequence.frame_list):
                    joints_dict[index] = human_pose_estimator.process_image(frame.getPixels())
                joints_dict_list.append(joints_dict)

            for index, joints in enumerate(joints_dict_list):
                probabilities = self.foul_analyzer.analyze_human_pose(joints)
                if probabilities[1] > 0.75:
                    contact_events[index].isFoul = True
                else:
                    contact_events[index].isFoul = False


        if appconfig.use_action_recognition:
            print("Use action recognition for foul recognition")
            for index, event in enumerate(contact_events):
                sequence = event.sequence
                event.foul_probabilities = self.foul_analyzer.analyze_action(sequence) # should deliver boolean or some datatype with probabilities for foul or not foul
                if event.foul_probabilities is not None and event.foul_probabilities[1] > event.foul_probabilities[0] and event.foul_probabilities[1] > 0.75:
                    event.isFoul = True
                else:
                    event.isFoul = False

        return contact_events