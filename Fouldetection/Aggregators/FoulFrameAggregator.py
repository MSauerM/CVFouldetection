from typing import List

from BasicFramework.Frame import Frame
from Fouldetection.DataStructures.ContactEvent import ContactEvent


class FoulFrameAggregator:

    def __init__(self):
        print("T")

    def aggregate(self, events: List[ContactEvent], frames: List[Frame]):
        for event in events:
            if event.isFoul is True:
                print("T")
                # draw on frames
            if event.isFoul is False:
                print("F")
                # draw on frames
        return frames