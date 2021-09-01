from __future__ import division

import argparse, time, logging, os, sys, math

import decord
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
    """
    Class for the encapsulation of the action recognition network
    ......

    Attributes
    -----------------
        ctx
            given context (CPU or GPU)
        net
            the neural network for action recognition itself
        train_file_name
            output file name to save the model parameters in case of training

    Methods
    -----------------
        train(dataset_location, training_file, train_epochs)
            trains/finetunes pretrained network by using the data at dataset_location
            specified by the training_file with the amount of epochs specified by
            train_epochs and finally saves the finetuned model parameters to a output file
        classify(sequence, frame_multiplier)
            analyzes the sequence by first using specific slicing technique for preparing
            the input in the net and then using the net for returning the net output as
            dictionary with 0 (no foul) and 1 (foul) as keys and probabilities for both
            categories
            frame_multiplier is optional and used if not every frame should be analyzed
        classify_test(video_filename, frame_multiplier)
            specific function for the test() method, which returns only the outcome with
            the highest probability (in contrast to the previous classify function)
        test(location, test_filename)
            function for getting the test accuracy by using the classify_test() function
            for each file at the given location specified inside the file named test_filename
            and comparing the expected results with the real outputs of the given net
    """

    def __init__(self, param_file=None):
        print("Init Action Recognizer")
        self.ctx = [mx.cpu()]
        self.net = get_model(name='i3d_resnet50_v1_kinetics400', nclass=2)
        now = datetime.now()
        nowstring = now.strftime("%d-%m-%y_%H-%M")
        self.train_file_name = "i3d {now}.params".format(now=nowstring)
        if param_file is not None:
            self.net.load_parameters(param_file, ctx = self.ctx)

    def train(self, dataset_location:str = '../Dataset_great', training_file:str = '../train_great 2 _ trim 3.txt', train_epochs: int = 5):
        print("Train")
        num_gpus = 1
        transform_train = video.VideoGroupTrainTransform(size=(224, 224), scale_ratios=[1.0, 0.8],
                                                         mean=[0.485, 0.456, 0.406], std=[0.299, 0.224, 0.255])
        per_device_batch_size = 5
        num_workers = 0
        batch_size = per_device_batch_size * num_gpus

        train_dataset = VideoClsCustom(root=os.path.expanduser(dataset_location),
                                       setting=os.path.expanduser(training_file),
                                       train=True,
                                       new_length=32,
                                       video_loader=True,
                                       use_decord=True,
                                       transform=transform_train)
        print('Load %d training samples.' % len(train_dataset))
        train_data = gluon.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers)
        self.net.collect_params().reset_ctx(self.ctx)
        print(self.net)

        lr_decay = 0.1
        lr_decay_epoch = [40, 80, 100]
        optimizer = 'sgd'
        optimizer_params = {'learning_rate': 0.001, 'wd': 0.0001, 'momentum': 0.9}
        trainer = gluon.Trainer(self.net.collect_params(), optimizer, optimizer_params) # self

        loss_fn = gluon.loss.SoftmaxCrossEntropyLoss()

        train_metric = mx.metric.Accuracy()
        train_history = TrainingHistory(['training-acc'])

        epochs = train_epochs  # 6#3
        lr_decay_count = 0

        for epoch in range(epochs):
            tic = time.time()
            train_metric.reset()
            train_loss = 0

            if epoch == lr_decay_epoch[lr_decay_count]:
                trainer.set_learning_rate(trainer.learning_rate * lr_decay)
                lr_decay_count += 1

            for i, batch in enumerate(train_data):
                data = split_and_load(batch[0], ctx_list=self.ctx, batch_axis=0)
                label = split_and_load(batch[1], ctx_list=self.ctx, batch_axis=0)

                with ag.record():
                    output = []
                    for _, X in enumerate(data):
                        X = X.reshape((-1,) + X.shape[2:])
                        pred = self.net(X)
                        output.append(pred)
                    loss = [loss_fn(yhat, y) for yhat, y in zip(output, label)]

                for l in loss:
                    l.backward()

                trainer.step(batch_size)

                train_loss += sum([l.mean().asscalar() for l in loss])
                train_metric.update(label, output)

                if i == 100:
                    break

            name, acc = train_metric.get()

            train_history.update([acc])
            print('[Epoch %d] train=%f loss=%f time: %f' %
                  (epoch, acc, train_loss / (i + 1), time.time() - tic))
        train_history.plot()

        self.net.save_parameters(self.train_file_name)

    def classify(self, sequence: Sequence, frame_multiplier = 1):
        frame_id_list = range(0, 32 * frame_multiplier, 1 *frame_multiplier)

        if len(sequence.frame_list) < 32:
            for i in range(len(sequence.frame_list), 32):
                sequence.frame_list.append(sequence.frame_list[-1])

        if len(sequence.frame_list) > 32:
            seq_frame_range = range(0, len(sequence.frame_list), 32)
            probabilities = {0: 0.0, 1: 0.0}
            for i in seq_frame_range:
                if i+32 < len(sequence.frame_list):
                    tmp_sequence = Sequence(sequence.frame_list[i:i + 32])
                    tmp_probabilities = self.classify(tmp_sequence)
                    if tmp_probabilities is not None and tmp_probabilities[1] > probabilities[1]:
                        probabilities = tmp_probabilities
                else:
                    last_sequence_count = len(sequence.frame_list) - i
                    tmp_sequence = Sequence(sequence.frame_list[i:i + last_sequence_count])
                    tmp_probabilities = self.classify(tmp_sequence)
                    if tmp_probabilities is not None and tmp_probabilities[1] > probabilities[1]:
                        probabilities = tmp_probabilities
            return probabilities

        if len(sequence.frame_list) == 32:
            try:
                clip_input = [sequence.frame_list[vid].get_pixels() for vid, _ in enumerate(frame_id_list)]

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


    def classify_test(self, video_filename, frame_multiplier = 1):
        vr = decord.VideoReader(video_filename)
        frame_id_list = range(0, 32 * frame_multiplier, 1*frame_multiplier)

        video_data = vr.get_batch(frame_id_list).asnumpy()

        clip_input = [video_data[vid, :, :, :] for vid, _ in enumerate(frame_id_list)]


        transform_fn = video.VideoGroupValTransform(size=224, mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])


        clip_input = transform_fn(clip_input)
        clip_input = np.stack(clip_input, axis=0)
        clip_input = clip_input.reshape((-1,) + (32, 3, 224, 224))
        clip_input = np.transpose(clip_input, (0, 2, 1, 3, 4))
        net_input = nd.array(clip_input)

        pred = self.net(net_input)

        classes = ['No Foul', 'Foul']
        topK = 2
        ind = nd.topk(pred, k=topK)[0].astype('int')
        print('The input video clip is classified to be')
        for i in range(topK):
            print('\t[%s], with probability %.3f.' %
                 (classes[ind[i].asscalar()], nd.softmax(pred)[0][ind[i]].asscalar()))
        return ind[0].asscalar()

    def test(self, location, test_filename):
        test_file= open(test_filename, 'r')
        lines = test_file.readlines()
        validation_values = []
        correct_results_counter = 0
        for line in lines:
            file_split = line.split()
            result = self.classify_test(location + file_split[0]+".mp4", frame_multiplier=1)
            validation_values.append([int(file_split[2]), result])

        for values in validation_values:
            if values[0] == values[1]:
                correct_results_counter += 1
        print("Number of Samples: {sample_number} ".format(sample_number=len(lines)))
        print("Correct Results: {correct_results}".format(correct_results = correct_results_counter))
        print("Validation Accuracy: {val_accuracy}".format(val_accuracy = correct_results_counter/len(lines)))


if __name__ == '__main__':
    actionrecognizer = ActionRecognizer("i3d 12-08-21_11-04.params")
    #actionrecognizer.train(dataset_location='D:/SOCCER_FOUL_DATA/Dataset_master', training_file='D:/SOCCER_FOUL_DATA/Dataset_master/train_1.txt', train_epochs=5)
    #actionrecognizer.classify("i3d 27-06-21_12-02.params", "../Dataset/foul_012.mp4", frame_multiplier=1)#"../Dataset_great/fair_054.mp4")#foul_092_Trim.mp4") #fair_054
    #actionrecognizer.classify_test("i3d 12-08-21_11-04.params", "fair_271.mp4")
    actionrecognizer.test("D:\SOCCER_FOUL_DATA\Dataset_master/", "D:/SOCCER_FOUL_DATA/Dataset_master/test_1.txt")
    #actionrecognizer.test("i3d 12-08-21_11-04.params", "../../../Dataset/", "../../../Dataset/test_1.txt")

