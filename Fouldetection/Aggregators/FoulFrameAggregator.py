from typing import List

from BasicFramework.Frame import Frame
from Fouldetection.DataStructures.ContactEvent import ContactEvent

from cv2 import cv2 as cv

class FoulFrameAggregator:

    def __init__(self):
        print("T")

    def aggregate(self, events: List[ContactEvent], frames: List[Frame]):
        for index, event in enumerate(events):
            for chain_member in event.bounding_box_chain.chain_members:
                x, y, w, h = chain_member.get_bounds()
                img = frames[chain_member.get_frame_index()].getPixels()
                color = None
                text = "ChainIndex: {chain_index}/ Foul: {foul_decision}"
                if event.isFoul is True:
                    color = (0, 255, 0)  # Foul will be displayed green
                    text = text.format(chain_index= index, foul_decision = "YES")
                elif event.isFoul is False:
                    color = (0, 0, 255) # No_Foul will be displayed red
                    text = text.format(chain_index= index, foul_decision = "NO")
                cv.rectangle(img, (x, y), (x+w, y+h), color, 3)
                cv.putText(img, text, (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        return frames