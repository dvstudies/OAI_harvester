#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import sqlite3
import argparse
import requests
import time
import os
import sys

db_name = 'biblhertz_02_2021_03.db'
img_url = "http://fotothek.biblhertz.it/bh/2048px/"

conn = sqlite3.connect(db_name, isolation_level=None, detect_types=sqlite3.PARSE_COLNAMES)
df = pd.read_sql_query("SELECT * FROM Objects", conn)

"""
getImages

Create a folder and store the images downloaded from their identifiers provided 
in the list of image identifiers given as a parameter

@param listIDs a list of digital image IDs
@return a list of image IDs for which it was not possible to download images
"""
def getImages(listImgs, img_url):
	print(f"Getting a total of {len(listImgs)} images from {img_url}")
	errorIDs = []
	#create a folder to store the images
	os.makedirs("biblhertz_images", exist_ok=True)
	print("Downloading images ", end="")
	for img_ in listImgs:
		response = requests.get(img_url+img_+".jpg")
		if response: #if the image request is positive, download the image in the local folder "images_bb"
			print("-", end="", flush=True)
			name = "biblhertz_images/"+str(img_)+".jpg"
			file = open(name, "wb")
			file.write(response.content)
			file.close()
		else:
			errorIDs.append(img_)
	return errorIDs

#Biblhertz_IMG_harvester.py --type Zeichnung Stadt Ort --artist --title --date_begin --date_end --medium
#if not --type then all

# defined command line options
# this also generates --help and error handling
parser=argparse.ArgumentParser()
parser.add_argument(
  "--type",  # name on the CLI - drop the `--` for positional/required parameters
  help="The type of object, in german with a capital letter (e.g. Zeichnung, Ort, Text)",
  nargs="*",  # 0 or more values expected => creates a list
  type=str,
  #default=[all],  # default if nothing is provided
)
parser.add_argument(
  "--artist",
  help="A name of an artist",
  nargs="*",
  type=str,  # any type/callable can be used here
  #default=[],
)
parser.add_argument(
  "--title",
  help="An artwork title",
  nargs="*",
  type=str,  # any type/callable can be used here
  #default=[],
)
parser.add_argument(
  "--date_begin",
  help="A starting date of creation (e.g. 1560)",
  nargs=1,
  type=int,  # any type/callable can be used here
  #default=[],
)
parser.add_argument(
  "--date_end",
  help="An ending date of creation (e.g. 1565)",
  nargs=1,
  type=int,  # any type/callable can be used here
  #default=[],
)
parser.add_argument(
  "--medium",
  help="The medium used for the artwork (e.g. Marmor, Öl & Holz, Papier)",
  nargs="*",
  type=str,  # any type/callable can be used here
  #default=[],
)
parser.add_argument(
	"--all",
	help="Set this argument if you want to download all available images from the database",
	nargs=1,
	type=bool,
	)
# parse the command line
args =parser.parse_args()
# access CLI options
img_list =[]
if args.type:
	print("Requested type: %r" % args.type)
	#img_list.append(df[(df['type'].isin(args.type)) & (df['img_digital']!='unavailable')]['type'])
	img_list.extend(list(df[(df['type'].str.contains('|'.join(args.type))) & (df['img_digital']!='unavailable')]['img_digital']))		  
if args.title:
	print("Requested title: %r" % args.title)
	img_list.extend(df[(df['title'].str.contains('|'.join(args.title))) & (df['img_digital']!='unavailable')]['img_digital'])
if args.artist:
	print("Requested artist: %r" % args.artist)
	img_list.extend(df[(df['artist'].str.contains('|'.join(args.artist))) & (df['img_digital']!='unavailable')]['img_digital'])
if args.date_begin:
	print("Requested date begin: %r" % args.date_begin)
	img_list.extend(df[(df['date_begin'].str.contains('|'.join(args.date_begin))) & (df['img_digital']!='unavailable')]['img_digital'])
if args.date_end:
	print("Requested date end: %r" % args.date_end)
	img_list.extend(df[(df['date_end'].str.contains('|'.join(args.date_end))) & (df['img_digital']!='unavailable')]['img_digital'])
if args.medium:
	print("Requested medium: %r" % args.medium)
	img_list.extend(df[(df['medium'].str.contains('|'.join(args.medium))) & (df['img_digital']!='unavailable')]['img_digital'])
if args.all:
	print("All available images will be downloaded from the database")
	img_list = list(df[df['img_digital']!='unavailable']['img_digital'])
if not img_list:
	print(f"No images were found for this request. If you need further information try: \n\npython Biblhertz_IMG_harvester.py --help\n\n")
else:
	errorIDs = getImages(img_list, img_url)
	print("The program was not able to download the following images:")
	print(errorIDs)

