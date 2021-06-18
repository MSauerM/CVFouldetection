from typing import List

import appconfig
from Fouldetection.ContactEvent import ContactEvent


class FoulRecognizer:

    def __init__(self):
        print("FoulRecognizer")

    def analyze(self, contact_events: List[ContactEvent]):
        print("Checking for possible fouls")
        if appconfig.use_human_pose_estimation:
            print("Use human pose estimation for foul recognition")
            joints_list = []
            ### Analyze loop
            for event in contact_events:
                sequence = event.sequence
                ##evaluate



        if appconfig.use_action_recognition:
            print("Use action recognition for foul recognition")


        return contact_events