import numpy as np
import logging
import sklearn
import pandas as pd
from sklearn.utils import class_weight
from simpletransformers.classification import ClassificationModel
import wandb
import torch

model = ClassificationModel('roberta', 'hope_speech_detector/eng_no_class_weights/',use_cuda=False)

"""
predictions, raw_outputs = model.predict(["Love your work.","You're ugly as fuck","fsbhfbsdqfbsdfhbqsfdihbshf"])
print(predictions)
"""

def is_hope_speech(txt):
    predictions, raw_outputs = model.predict([txt])
    return predictions[0]

def label_hope(post):
    post.label_hope_as(is_hope_speech(post.txt))
    return post

def label_hope_list(post_list):
    texts = [p.txt for p in post_list]
    predictions, raw_outputs = model.predict(texts)

    for i in range(len(post_list)):
        post_list[i].label_hope_as(predictions[i])

    return post_list
