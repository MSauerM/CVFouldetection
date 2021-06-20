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
            for index, event in enumerate(contact_events):
                sequence = event.sequence
                joints_dict = dict()
                for frame in sequence.frame_list:
                    joints_dict[index] = human_pose_estimator.estimate(frame)
                joints_dict_list.append(joints_dict)

            for joints in joints_dict_list:
                self.foul_analyzer.analyze_human_pose(joints)


        if appconfig.use_action_recognition:
            print("Use action recognition for foul recognition")
            for index, event in enumerate(contact_events):
                sequence = event.sequence
                self.foul_analyzer.analyze_action(sequence) # should deliver boolean or some datatype with probabilities for foul or not foul
                event.isFoul = True

        return contact_events