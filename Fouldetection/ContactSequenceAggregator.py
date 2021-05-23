from typing import List

from CVUtility.BoundingBoxInformation import BoundingBoxInformation


class ContactSequenceAggregator:

    def __init__(self):
        print("ContactSequenceAggregator")

    def aggregate(self, frame_list, bounding_boxes:List[BoundingBoxInformation]):
        print("Aggregate")
        # return a sequence which is aggregated form of the bounding boxes out of the frames in the frame_list
        for box in bounding_boxes:
            print(box)
            #get Image of the relevant frame
            #box.get_frame_index()

        return None
