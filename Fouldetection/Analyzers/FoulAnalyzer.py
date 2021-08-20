import cv2

import appconfig
from Fouldetection.Analyzers.ActionRecognizer import ActionRecognizer
import numpy as np
from cv2 import cv2 as cv

class FoulAnalyzer:

    def __init__(self):
        print("Init FoulAnalyzer")
        if appconfig.use_action_recognition:
            self.action_recognizer = ActionRecognizer("./Fouldetection/Analyzers/i3d 12-08-21_11-04.params")

    def analyze_human_pose(self, joints: dict):
        print("Analyze Foul based on Human Pose")
        # joints contains dictionary for frame with the corresponding joints
        # print(""joints[0])
        print(joints)
        # change nd array to normal array
        distance_matrix_list = []
        #angle_skeleton_list = []
        skeleton_info_dict = dict()
        for key in joints:
            # print(joints[key][0]) Skelettebene
            # joints[key][1] confidences für jeweiliges Skelett
            if joints[key] is not None:
                print(joints[key][0].shape[0])
                distance_matrix = np.empty((joints[key][0].shape[0], joints[key][0].shape[0]))
                skeleton_info_dict[key] = []
                if joints[key][0].shape[0] > 1: # Anzahl der Skelette muss höher als 1 sein
                    # Berechnung des Nähekoeffizienten
                    for z in range(0, joints[key][0].shape[0]-1):
                        box = cv.minAreaRect(joints[key][0][z])
                        box_points = cv.boxPoints(box)
                        box_angle = box[2]
                        if box[1][0] < box[1][1]:
                            box_angle += 180
                        else:
                            box_angle += 90
                        box_points = np.int0(box_points)
                        #angle_skeleton_list.append([z, box_angle, box[0], box_points])
                        skeleton_info_dict[key].append([z, box_angle, np.array([box[0][0], box[0][1]]), box_points]) # index, angle, center, points, (width, height)
                        for d in range (z, joints[key][0].shape[0]):
                            #skelett 1
                            skeleton1 = joints[key][0][z]
                            #skelett 2
                            skeleton2 = joints[key][0][d]
                            #box2 = cv.minAreaRect(skeleton2)
                            #box2_angle = box2[2]
                            #box2_points = cv.boxPoints(box2)
                            #box2_points = np.int0(box2_points)
                            distance = 0.0
                            distance_counter = 0
                            for a in skeleton1:
                                for b in skeleton2:
                                    # Differenzen quadrieren
                                    #print(a)
                                    #print(b)
                                    # Magnitude bilden
                                    e = a - b
                                    distance += np.sqrt(e.dot(e))
                                    distance_counter += 1
                            distance_matrix[z][d] = distance / distance_counter
                            distance_matrix[d][z] = distance / distance_counter
                    #for i in range(z, joints[key][0].shape[1]):
                    distance_matrix_list.append(distance_matrix)
                else:
                    distance_matrix_list.append(None) # evtl. []
                    skeleton_info_dict[key] = None # evtl. []
                #print("Test")
            else:
                distance_matrix_list.append(None)
                skeleton_info_dict[key] = None

        # Verketten der Skeletons, um Listen aus Angles zu erhalten
        chain_dict_list = []
        for index in skeleton_info_dict:
            if skeleton_info_dict[index] is not None:
                for i in range(0, len(skeleton_info_dict[index])):
                    #angle_list = []
                    #angle_list.append([index, i, skeleton_info_dict[index][i][1]])
                    chain_dict = dict()
                    chain_dict[index] = i
                    last_chain = [index, i] # frame, skelett index
                    #skeleton_info_dict = None
                    for walk_index in range(index + 1, len(skeleton_info_dict)):
                        if skeleton_info_dict[walk_index] is None:
                            break
                        next_index = -1
                        min_distance = 100000
                        for z in range(0, len(skeleton_info_dict[walk_index])):
                            distance_vector = skeleton_info_dict[walk_index][z][2] - skeleton_info_dict[last_chain[0]][last_chain[1]][2] # error here because of - for tuples
                            distance_magnitude = np.sqrt(distance_vector.dot(distance_vector))#0 ##### TODO: Implement vector magnitude here
                            if distance_magnitude < min_distance and distance_magnitude <20:
                                next_index = z
                                min_distance = distance_magnitude
                        if next_index == -1:
                            break
                        else:
                            chain_dict[walk_index] = next_index
                            last_chain = [walk_index, next_index]
                    chain_dict_list.append(chain_dict)

        # Testen ob bei diesem Skeletons eine Winkeländerung größer als Threshold auftritt

        for chain_dictionary in chain_dict_list:
            # info for this dictionary
            angle_list = []
            width_height_list =[]
            isCloseEnough = False
            isFalling = False
            for item in chain_dictionary:
                # access distance matrix at certain frame
                distance_matrix_cut = distance_matrix_list[item][chain_dictionary[item]]

                for element in distance_matrix_cut:
                    if element < 50:
                        isCloseEnough = True
                        break

                # access skeleton_info_dict for angles
                skeleton_info = skeleton_info_dict[item][chain_dictionary[item]]
                angle_list.append(skeleton_info[1])


            for index in range(0, len(angle_list)-1):
                if abs(angle_list[index] - angle_list[index + 1]) > 60: # potential error here
                    isFalling = True
                    break
            #for index in range(0, len(width_height_list)-1):
            #    if abs(width_height_list[index][0] - width_height_list[index+1][0]) > 30 or  abs(width_height_list[index][1] - width_height_list[index+1][1]) > 30:
            #        isFalling = True
            #        break

            if isFalling and isCloseEnough:
                return {0: 0.00, 1: 1.00}

        return {0: 1.00, 1: 0.00}


    def analyze_action(self, sequence):
        print("Analyze Foul based on Action Recognition")
        probabilities = self.action_recognizer.classify(sequence)
        print(probabilities)
        return probabilities
