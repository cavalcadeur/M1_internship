# -*- coding: utf-8 -*-

import sys
import os
import argparse
import csv
import json

#from hate_detector import label_hate
from hope_detector import *
from topic_detector import label_topic_list

from post import *

def main():
    parser = argparse.ArgumentParser(
        description='A script to update a csv already')
    parser.add_argument('-i','--infile',
        help='File containing the various posts',
        default='posts.csv')
    parser.add_argument('-o', '--outfile',
        help='The output file',
        default='output')
    parser.add_argument('-d', '--detectiontype',
        help='The type of detection to do (hateSpeech,hopeSpeech,topic)',
        default='topic')
    parser.add_argument('-n','--topicNumber',
        help='Number of topics to detect',
        default='8')
    args = parser.parse_args()


    posts = open_csv(args.infile)

    if args.detectiontype == "hateSpeech":
        print("If you want to detect hate speech, you should use update_database.py instead. Sorry for the inconvenience.")
    elif args.detectiontype == "hopeSpeech":
        posts = label_hope_list(posts)
    elif args.detectiontype == "topic":
        posts = label_topic_list(posts,args.topicNumber)

    save_csv(posts,args.outfile)


if __name__ == "__main__":
    main()
