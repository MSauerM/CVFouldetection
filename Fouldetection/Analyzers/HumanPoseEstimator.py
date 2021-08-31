from __future__ import division

from matplotlib import pyplot as plt
from gluoncv import model_zoo, data, utils
from gluoncv.data.transforms.pose import detector_to_alpha_pose, heatmap_to_coord_alpha_pose

import argparse, time, logging, os, math, tqdm, cv2

import numpy as np
import mxnet as mx
from mxnet import gluon, nd, image
from mxnet.gluon.data.vision import transforms

import gluoncv as gcv
from gluoncv import data
from gluoncv.data import mscoco
from gluoncv.model_zoo import get_model
from gluoncv.data.transforms.pose import detector_to_simple_pose, heatmap_to_coord
from gluoncv.utils.viz import cv_plot_image, cv_plot_keypoints

import appconfig


class HumanPoseEstimator:
    """
        Class for ....
        ......

        Attributes
        -----------------



        Methods
        -----------------

        """
    def __init__(self):
        self.ctx = mx.cpu()
        self.detector = model_zoo.get_model('yolo3_mobilenet1.0_coco', pretrained=True)
        self.pose_net = model_zoo.get_model('alpha_pose_resnet101_v1b_coco', pretrained=True)
        self.detector.reset_class(["person"], reuse_weights=['person'])

    def process_image(self, input_img: nd.array):
        input_img = mx.nd.array(cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)).astype('uint8')
        x, img = gcv.data.transforms.presets.ssd.transform_test(input_img, short=512, max_size=350)
        x = x.as_in_context(self.ctx)

        class_IDs, scores, bounding_boxs= self.detector(x)
        pose_input, upscale_bbox = detector_to_alpha_pose(img, class_IDs, scores, bounding_boxs) # alternativ auch simplePose

        if pose_input is not None:
            predicted_heatmap = self.pose_net(pose_input)
            pred_coords, confidence = heatmap_to_coord_alpha_pose(predicted_heatmap, upscale_bbox)
            if appconfig.show_debug_plots:
                ax = utils.viz.plot_keypoints(img, pred_coords, confidence, class_IDs, bounding_boxs, scores, box_thresh=0.5, keypoint_thresh=0.2)
                plt.show()
            return pred_coords.asnumpy(), confidence
        return None


if __name__ == '__main__':
    poseEstimator = HumanPoseEstimator()
    img = cv2.imread("./testbild1.png")
    poseEstimator.process_image(img)