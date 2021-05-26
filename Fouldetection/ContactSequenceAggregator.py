from typing import List

from BasicFramework.Frame import Frame
from BasicFramework.Sequence import Sequence
from CVUtility.BoundingBoxInformation import BoundingBoxInformation
from Fouldetection.BoundingBoxInformationChain import BoundingBoxInformationChain
import numpy as np


class ContactSequenceAggregator:

    def __init__(self):
        print("ContactSequenceAggregator")

    def aggregate(self, frame_list:List[Frame], bounding_boxes:dict):
        print("Aggregate")
        # find the lowest and the highest frame index to get bounds for a range
        #lowest_index = min(box.get_frame_index() for box in bounding_boxes)
        #highest_index = max(box.get_frame_index() for box in bounding_boxes)
        #print(lowest_index)
        #print(highest_index)
        bounding_box_chains = self._build_chains(bounding_boxes)


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

    def _build_chains(self, bounding_boxes: dict):
        bounding_boxes_range = range(len(bounding_boxes))
        chains = []
        for i in bounding_boxes_range:  # 1. Schleife
            #horizontal_layer = bounding_boxes[i]
            removal_list = []
            for y in range(0, len(bounding_boxes[i])):
                new_chain = BoundingBoxInformationChain()
                starting_link = bounding_boxes[i][y]
                new_chain.add(starting_link)
                removal_list.append((i, y))
                isChained = False
                for z in range(i+1, len(bounding_boxes)):
                    if not bounding_boxes[z]:
                        break
                    magnitude = 10000
                    index = -1
                    for x in range(0, len(bounding_boxes[z])):
                        distanceVector = bounding_boxes[z][x].get_midpoint() - starting_link.get_midpoint()
                        distance_magnitude = np.linalg.norm(distanceVector)
                        if distance_magnitude < magnitude and distance_magnitude < 3:
                            index = x
                            magnitude = distance_magnitude
                    if index is not -1:
                        starting_link = bounding_boxes[z][index]
                        new_chain.add(starting_link)
                        removal_list.append((z, index))
                    else:
                        # chain is broken
                        break
                chains.append(new_chain)

            removal_list.sort(key= lambda x: x[1], reverse=True)
            for remove_counter in range(0, len(removal_list)):
                remove_tuple = removal_list[remove_counter]
                del bounding_boxes[remove_tuple[0]][remove_tuple[1]]

        return chains
    # Bounding Box Chaining
    # aggregate bounding Boxes to relevant chains

    def _build_new_chain(self, frame_index, list_index, bounding_boxes: dict) -> BoundingBoxInformationChain:
        chain = BoundingBoxInformationChain()
        start_bb = bounding_boxes[frame_index][list_index]
        list_for_removal = []
        list_for_removal.append((frame_index, list_index))
        chain.add(start_bb)
        for i in range(frame_index+1, len(bounding_boxes)):
            if bounding_boxes[i]:
                index = -1
                magnitude = 1000.0
                for x in range(0, len(bounding_boxes[frame_index])):
                    distance_vector = bounding_boxes[i][x].get_midpoint() - start_bb.get_midpoint()
                    distance = np.linalg.norm(distance_vector)
                    if distance < 50 and distance < magnitude:
                        index = x
                        magnitude = distance
                if index != -1:
                    start_bb = bounding_boxes[i][index]
                    chain.add(start_bb)
                    list_for_removal.append((i, index))
                else:
                    break
            else:
                break

        return chain


'''     index_range = range(lowest_index, highest_index)
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
'''
