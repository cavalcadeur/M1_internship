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

def extract_posts(reader,source="youtube"):
    first_line = True
    posts_list = []
    head = []
    for row in reader:
        if first_line and source == "youtube": # Only for csv files must we ignore the first line
            first_line = False
            head = list(row)
            continue
        new_post = Post()
        new_post.get_data_from_csv(row,source,head)
        posts_list.append(new_post)

    return posts_list

def process_file(fileName,source="youtube"):

    if source == "youtube": # Then it is a csv file
        with open(fileName, newline='') as my_file:
            reader = csv.reader(my_file, delimiter='\t')
            posts_list = extract_posts(reader,source)

    else:
        my_file = json.load(open(fileName, "r"))
        posts_list = extract_posts(my_file,source)

    if len(posts_list) == 0:
        return posts_list

    #posts_list = label_hope_list(posts_list)

    for p in posts_list:
        p = label_hate(p)
        #p = label_topic(p)
        if p.is_hopeful():
            print(p)
            print("------------")

    return posts_list


def main():
    parser = argparse.ArgumentParser(
        description='A script to detect hate_speech in posts classified according to their topic.')
    parser.add_argument('-i','--infile',
        help='File containing the various posts',
        default='posts.csv')
    parser.add_argument('-o', '--outfile',
        help='The output directory',
        default='output')
    parser.add_argument('-p', '--posttype',
        help='The type of posts (youtube,facebook)',
        default='youtube')
    parser.add_argument("--dir", help="extract from an entire directory instead of just one file, the directory path is indicated by --infile",action="store_true")
    args = parser.parse_args()


    if not os.path.isfile(args.outfile):
        os.mknod(args.outfile)
        print(f'Created file: {args.outfile}')

    posts = []

    if args.dir:
        for entry in os.scandir(args.infile):
            if entry.is_dir():
                continue
            posts += process_file(entry.path,args.posttype)
    else:
        posts += process_file(args.infile,args.posttype)


    with open(args.outfile, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='\t',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['id','text','isHate','topic','isHope'])
        for i in range(len(posts)):
            spamwriter.writerow([i] + posts[i].get_csv())



if __name__ == "__main__":
    main()
