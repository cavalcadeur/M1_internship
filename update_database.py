# -*- coding: utf-8 -*-

import sys
import os
import argparse
import csv
import json

from hate_detector import label_hate
#from hope_detector import *
#from topic_detector import label_topic
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
        default='hateSpeech')
    args = parser.parse_args()


    posts = open_csv(args.infile)

    if args.detectiontype == "hateSpeech":
        for p in posts:
            p = label_hate(p)
    elif args.detectiontype == "hopeSpeech":
        print("If you want to detect hope speech, you should use update_database_bis.py instead. Sorry about this.")
    elif args.detectiontype == "topic":
        print("If you want to detect topic, you should use update_database_bis.py instead. Sorry about this.")


    save_csv(posts,args.outfile)



if __name__ == "__main__":
    main()
