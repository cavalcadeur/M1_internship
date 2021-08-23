import sys
import os
import argparse
import csv
import json
import random
import math

#from update_database import open_csv
from post import *

def main():
    parser = argparse.ArgumentParser(
        description='A script to manually add label to a csv')
    parser.add_argument('-i','--infile',
        help='File containing the various posts',
        default='posts.csv')
    parser.add_argument('-o','--outfile',
        help='File for saving the human labeled results',
        default='posts.csv')
    parser.add_argument('-d', '--detectiontype',
        help='The type of detection to label (hateSpeech,hopeSpeech)',
        default='hateSpeech')
    parser.add_argument('-s', '--samplesize',
        help='The number of posts to label',
        default='100')

    args = parser.parse_args()

    posts = open_csv(args.infile)

    print("\nPlease label each of these 0 or 1.\n")

    indexes = [i for i in range(len(posts))]
    random.shuffle(indexes)

    labeled = []
    not_labeled = []

    for i in indexes:
        if (posts[i].is_hateful() and args.detectiontype == "hateSpeech") or (posts[i].is_hopeful() and args.detectiontype == "hopeSpeech"):
            labeled.append(i)
        else:
            not_labeled.append(i)

    # Ok so now we can have a more homogenous repartition of labels
    n = int(args.samplesize)
    h = math.ceil(n / 2)
    if len(labeled) > h and len(not_labeled) > h:
        ids = labeled[:h] + not_labeled[:h]
        random.shuffle(ids)
    else:
        print("FINISH ME YOU FOOL !")
        print(len(labeled))
        return



    labels = [0,0,0,0] # 0 : label non-hate and non-hate 1 : label hate and non-hate 2 : label non hate but hate 3 : label hate and hate

    for i in range(int(args.samplesize)):
        answer = input(posts[ids[i]].txt + " ")
        while not answer in ["0","1"]:
            answer = input("")
        if args.detectiontype == "hateSpeech":
            j = int(answer) * 2
            if posts[ids[i]].is_hateful():
                j += 1
        else:
            j = int(answer) * 2 + (1 if posts[ids[i]].is_hopeful() else 0)

        posts[ids[i]].realHate = answer

        labels[j] += 1
        print(posts[ids[i]].is_hateful(),"\n ------------------------- \n")

    print(labels)


    save_csv(posts,args.outfile)


if __name__ == "__main__":
    main()
