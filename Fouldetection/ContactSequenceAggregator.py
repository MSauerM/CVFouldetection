from typing import List

from BasicFramework.Frame import Frame
from BasicFramework.Sequence import Sequence
from CVUtility.BoundingBoxInformation import BoundingBoxInformation
from Fouldetection.BoundingBoxInformationChain import BoundingBoxInformationChain


class ContactSequenceAggregator:

    def __init__(self):
        print("ContactSequenceAggregator")

    def aggregate(self, frame_list:List[Frame], bounding_boxes:dict):
        print("Aggregate")
        # find the lowest and the highest frame index to get bounds for a range
        lowest_index = min(box.get_frame_index() for box in bounding_boxes)
        highest_index = max(box.get_frame_index() for box in bounding_boxes)
        print(lowest_index)
        print(highest_index)

# Bounding Box Chaining
        # aggregate bounding Boxes to relevant chains
        index_range = range(lowest_index, highest_index)
        current_frame_bounding_boxes = []
        next_frame_bounding_boxes = []
        bounding_box_chains = []
        for index in index_range:
            # find all bounding box with the corresponding index
            # check index is lowest index, because for the first time the bounding boxes of the next frame can't be
            # the current one
            if index is lowest_index:
                #find initial frame bounding boxes
                current_frame_bounding_boxes = self._find_bounding_boxes_by_index(bounding_boxes, index)

            if not bounding_box_chains:
                for box in current_frame_bounding_boxes:
                    chain = BoundingBoxInformationChain()
                    chain.add(box)
                    bounding_box_chains.append(chain)

            #find all bounding boxes with the next index
            next_frame_bounding_boxes = self._find_bounding_boxes_by_index(bounding_boxes, index+1)

            #current_frame_bounding_boxes = next_frame_bounding_boxes

            for chain in bounding_box_chains:
                chain_link = chain.search_for_new_chain_link(next_frame_bounding_boxes)
                if chain_link:
                    next_frame_bounding_boxes.remove(chain_link)

            for chain in bounding_box_chains:
                for box in next_frame_bounding_boxes:
                    if not chain.contains(box):
                        new_chain = BoundingBoxInformationChain()
                        new_chain.add(box)
                        bounding_box_chains.append(new_chain)
                        break

# Sequence Building out of bounding box chains
        sequences = []

        for chain in bounding_box_chains:
            sequence_frames = []
            for link in chain.chain_members:
                # find the image from the frame list
                img = frame_list[link.get_frame_index()]
                # retrieve bounds
                (x, y, w, h) = link.get_bounds()
                # crop the image
                img_crop = img[y:y+h, x:x+w]

                cropped_frame = Frame(img.getTimestamp(), img_crop, img.getFrameCount())
                sequence_frames.append(cropped_frame)
            sequence = Sequence(sequence_frames)
            sequences.append(sequence)

        return sequences

    # split bounding box by index reorders the list of bounding boxes to a dictionary where the key contains a list as value
    # and in this list there are the bounding Boxes of the frame
    # theoretisch könnte man diesen Schritt auch zu einem früheren Punkt machen, allerdings würde dies dann wieder die
    # vorherigen Prozesse beeinflussen
    def _split_bounding_box_by_index(self, bounding_boxes: List[BoundingBoxInformation]):

        return None

    #alternative, less efficient approach in comparison to the one above
    def _find_bounding_boxes_by_index(self, bounding_boxes: List[BoundingBoxInformation], index):
        boxes = []
        for box in bounding_boxes:
            if box.get_frame_index() is index:
                boxes.append(box)
        return boxes