import cv2

import appconfig
from Fouldetection.Analyzers.ActionRecognizer import ActionRecognizer
import numpy as np
from cv2 import cv2 as cv

class FoulAnalyzer:

    def __init__(self):
        print("Init FoulAnalyzer")
        if appconfig.use_action_recognition:
            self.action_recognizer = ActionRecognizer("./Fouldetection/Analyzers/i3d 27-06-21_12-02.params")

    def analyze_human_pose(self, joints: dict):
        print("Analyze Foul based on Human Pose")
        # joints contains dictionary for frame with the corresponding joints
        # print(""joints[0])
        print(joints)
        # change nd array to normal array
        distance_matrix_list = []
        angle_skeleton_list = []
        for key in joints:
            # print(joints[key][0]) Skelettebene
            # joints[key][1] confidences für jeweiliges Skelett
            print(joints[key][0].shape[0])
            distance_matrix = np.empty((joints[key][0].shape[0], joints[key][0].shape[0]))
            if joints[key][0].shape[0] > 1: # Anzahl der Skelette muss höher als 1 sein
                # Berechnung des Nähekoeffizienten

                for z in range(0, joints[key][0].shape[0]-1):
                    box = cv.minAreaRect(joints[key][0][z])
                    box_points = cv.boxPoints(box)
                    box_angle = box[2]
                    box_points = np.int0(box_points)
                    angle_skeleton_list.append([z, box_angle, box[0], box_points])
                    for d in range (1, joints[key][0].shape[0]):
                        #skelett 1
                        skeleton1 = joints[key][0][z]
                        #skelett 2
                        skeleton2 = joints[key][0][z+d]
                        #box2 = cv.minAreaRect(skeleton2)
                        #box2_angle = box2[2]
                        #box2_points = cv.boxPoints(box2)
                        #box2_points = np.int0(box2_points)
                        distance = 0.0
                        distance_counter = 0
                        for a in skeleton1:
                            for b in skeleton2:
                                # Differenzen quadrieren
                                print(a)
                                print(b)
                                # Magnitude bilden
                                e = a - b
                                distance += np.sqrt(e.dot(e))
                                distance_counter += 1
                        distance_matrix[z][z+d] = distance / distance_counter
                #for i in range(z, joints[key][0].shape[1]):
                distance_matrix_list.append(distance_matrix)
            else:
                distance_matrix_list.append(None) # evtl. []
                angle_skeleton_list.append(None) # evtl. []
            print("Test")

        # Verketten der Skeletons

        # Testen ob bei diesem Skeletons eine Winkeländerung größer als Threshold auftritt



    def analyze_action(self, sequence):
        print("Analyze Foul based on Action Recognition")
        probabilities = self.action_recognizer.classify(sequence)
        print(probabilities)
        return probabilities
