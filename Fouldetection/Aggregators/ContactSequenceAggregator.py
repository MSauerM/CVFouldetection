from typing import List

import appconfig
from BasicFramework.Frame import Frame
from BasicFramework.Sequence import Sequence
from Fouldetection.DataStructures.BoundingBoxInformation import BoundingBoxInformation
from Fouldetection.DataStructures.BoundingBoxInformationChain import BoundingBoxInformationChain
import numpy as np


class ContactSequenceAggregator:
    """
        Class for ....
        ......

        Attributes
        -----------------



        Methods
        -----------------

        """
    maximal_distance = 250
    break_limit = 5

    def __init__(self):
        print("ContactSequenceAggregator")

    def aggregate(self, frame_list:List[Frame], bounding_boxes:dict):
        print("Aggregate")
        # find the lowest and the highest frame index to get bounds for a range
        bounding_box_chains = self._build_chains(bounding_boxes)
        # Sequence Building out of bounding box chains
        sequences = []

        for chain in bounding_box_chains:
            sequence_frames = []
            if appconfig.cropping_strategy is appconfig.CroppingStrategy.DYNAMIC_VARIED:
                for link in chain.chain_members:
                    # find the image from the frame list
                    img = frame_list[link.get_frame_index()]
                    # retrieve bounds
                    (x, y, w, h) = link.get_bounds()
                    # crop the image
                    img_crop = img.get_pixels()[y:y + h, x:x + w] # dynamic with variable size

                    cropped_frame = Frame(img.get_timestamp(), img_crop, img.get_frame_index())
                    sequence_frames.append(cropped_frame)
                sequence = Sequence(sequence_frames)
                sequences.append(sequence)

            if appconfig.cropping_strategy is appconfig.CroppingStrategy.DYNAMIC_FIXED:
                fixed_size = [0, 0]
                if appconfig.preferred_size_dynamic_fixed is not None:
                    fixed_size[0] = appconfig.preferred_size_dynamic_fixed
                    fixed_size[1] = appconfig.preferred_size_dynamic_fixed
                else:
                    for link in chain.chain_members:
                        (x, y, w, h) = link.get_bounds()
                        if fixed_size[0] < w:
                            fixed_size[0] = w
                        if fixed_size[1] < h:
                            fixed_size[1] = h

                w = fixed_size[0]
                h = fixed_size[1]
                for link in chain.chain_members:
                    # find the image from the frame list
                    img = frame_list[link.get_frame_index()]
                    # retrieve bounds
                    midpoint = link.get_midpoint()
                    # crop the image

                    x = int(midpoint[0] - (w/2))
                    y = int(midpoint[1] - (h/2))
                    img_height = img.get_dimensions()[0]
                    img_width = img.get_dimensions()[1]
                    # testing if the midpoint is in the border area
                    if x < appconfig.preferred_size_dynamic_fixed / 2:
                        x = int(appconfig.preferred_size_dynamic_fixed / 2)
                    if x > img_width - (appconfig.preferred_size_dynamic_fixed / 2):
                        x = int(img_width - (appconfig.preferred_size_dynamic_fixed / 2))
                    if y < appconfig.preferred_size_dynamic_fixed / 2:
                        y = int(appconfig.preferred_size_dynamic_fixed / 2)
                    if y > img_height - (appconfig.preferred_size_dynamic_fixed / 2):
                        y = int(img_height - (appconfig.preferred_size_dynamic_fixed/2))

                    img_crop = img.get_pixels()[y:y + h, x:x + w]  # dynamic fixed size

                    cropped_frame = Frame(img.get_timestamp(), img_crop, img.get_frame_index())
                    sequence_frames.append(cropped_frame)
                sequence = Sequence(sequence_frames)
                sequences.append(sequence)

            if appconfig.cropping_strategy is appconfig.CroppingStrategy.STATIONARY:
                stationary_size = [20000, 20000, 0, 0] # lower_x, lower_y, upper_x, upper_y
                for link in chain.chain_members:
                    (x, y, w, h) = link.get_bounds()

                    if stationary_size[0] > x:
                        stationary_size[0] = x
                    if stationary_size[1] > y:
                        stationary_size[1] = y
                    if stationary_size[2] < (x + w):
                        stationary_size[2] = x + w
                    if stationary_size[3] < (y + h):
                        stationary_size[3] = y + h
                for link in chain.chain_members:
                    # find the image from the frame list
                    img = frame_list[link.get_frame_index()]
                    img_crop = img.get_pixels()[stationary_size[1]:stationary_size[3], stationary_size[0]:stationary_size[2]]  # dynamic fixed size

                    cropped_frame = Frame(img.get_timestamp(), img_crop, img.get_frame_index())
                    sequence_frames.append(cropped_frame)
                sequence = Sequence(sequence_frames)
                sequences.append(sequence)

        return sequences, bounding_box_chains

    def _build_chains(self, bounding_boxes: dict):
        bounding_boxes_range = range(len(bounding_boxes))
        chains = []
        for i in bounding_boxes_range:  # 1. Schleife
            removal_list = []
            max_length = len(bounding_boxes[i])
            while bounding_boxes[i]:
                chains.append(self._build_new_chain(i, 0, bounding_boxes))

        return chains

    def _build_new_chain(self, frame_index, list_index, bounding_boxes: dict) -> BoundingBoxInformationChain:
        chain = BoundingBoxInformationChain()
        dictionary_length = len(bounding_boxes)
        start_bb = bounding_boxes[frame_index][list_index]
        list_for_removal = []
        list_for_removal.append((frame_index, list_index))
        chain.add(start_bb)
        break_counter = 0
        for i in range(frame_index+1, len(bounding_boxes)):
            if bounding_boxes[i]:
                index = -1
                magnitude = 1000.0
                list_length = len(bounding_boxes[i])
                x = 0
                while bounding_boxes[i] and x < list_length:
                    distance_vector = bounding_boxes[i][x].get_midpoint() - start_bb.get_midpoint()
                    distance = np.linalg.norm(distance_vector)
                    if distance < self.maximal_distance and distance < magnitude: #distance < magnitude: #
                        index = x
                        magnitude = distance
                    x += 1
                if index != -1:
                    break_counter = 0
                    start_bb = bounding_boxes[i][index]
                    chain.add(start_bb)
                    list_for_removal.append((i, index))
                else:
                    break_counter += 1
                    if break_counter >= self.break_limit:
                        break
            else:
                break_counter += 1
                if break_counter >= self.break_limit:
                    break

        list_for_removal.sort(key=lambda x:x[1], reverse=True)
        for remove_counter in range(0, len(list_for_removal)):
            remove_tuple = list_for_removal[remove_counter]
            del bounding_boxes[remove_tuple[0]][remove_tuple[1]]

        return chain
