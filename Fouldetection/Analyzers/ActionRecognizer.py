from __future__ import division

import argparse, time, logging, os, sys, math

#import decord
import numpy as np
import mxnet as mx
import gluoncv as gcv
from mxnet import gluon, nd, init, context
from mxnet import autograd as ag
from mxnet.gluon import nn
from mxnet.gluon.data.vision import transforms

from gluoncv.data.transforms import video
from gluoncv.data import VideoClsCustom
from gluoncv.model_zoo import get_model
from gluoncv.utils import makedirs, LRSequential, LRScheduler, split_and_load, TrainingHistory

from datetime import datetime

from cv2 import cv2

from BasicFramework.Sequence import Sequence


class ActionRecognizer:

    def __init__(self, param_file):
        print("Init Action Recognizer")
        self.ctx = [mx.cpu()]
        self.net = get_model(name='i3d_resnet50_v1_kinetics400', nclass=2)
        if param_file is not None:
            self.net.load_parameters(param_file, ctx = self.ctx)

# maybe renaming it to get probabilities or something like that
    def classify(self, sequence: Sequence, frame_multiplier = 1):
        frame_id_list = range(0, 32 * frame_multiplier, 1 *frame_multiplier)

        if len(sequence.frame_list) <32:
            for i in range(len(sequence.frame_list), 32):
                sequence.frame_list.append(sequence.frame_list[-1])

        if len(sequence.frame_list) >= 32:
            try:
                clip_input = [sequence.frame_list[vid].getPixels() for vid, _ in enumerate(frame_id_list)]

                transform_fn = video.VideoGroupValTransform(size=224, mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
                clip_input = transform_fn(clip_input)
                clip_input = np.stack(clip_input, axis=0) # clip_input must have the same shape
                clip_input = clip_input.reshape((-1,) + (32, 3, 224, 224))
                clip_input = np.transpose(clip_input, (0, 2, 1, 3, 4))
                net_input = nd.array(clip_input)

                pred = self.net(net_input)
                classes = ['No Foul', 'Foul']
                topK = 2
                ind = nd.topk(pred, k = topK)[0].astype('int')
                probabilities = dict()
                for i in range(topK):
                    k = ind[i].asscalar() # classified label as scalar
                    kclass = classes[k] # name of label
                    prob = nd.softmax(pred)[0][ind[i]].asscalar() # probability amount for this scalar label
                    probabilities[k] = prob
                    print('\t[%s], with probability %.3f.' %
                          (kclass, prob))

                return probabilities
            except ValueError:
                print("ValueError")
        else:
            return None
