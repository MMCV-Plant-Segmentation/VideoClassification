# this is /deltos/e/pointillist_maize/code/video_classification/interactive_plot.py
#
# modified from /deltos/e/pointillist_maize/code/video_classification/flightpathonefile.py
# Evie Wilbur, spring, 2025
#

# to include elapsed time and frame numbers for each point
# to make it easier to find a complete cycle without relying
# on the coordinates being in close proximiity.
#
# Fluharty, Ersoy, and Kazic, 27.1.2026

# per google AI summary when querying
# "matplotlib add annotations to points in line plot as tooltips"
#
# srt is a third-party package for parsing SRT files that puts all the data on one line
# https://srt.readthedocs.io/en/latest/quickstart.html
# thanks, Chris!


# to run from the python command line (REPL):
#
# from pathlib import Path
# from interactive_plot import process_video_data
#
# call is:
# process_video_data(Path('/deltos/f/aerial_imaging/images/24r/grace/30.9/DJI_0309.SRT'))


import sys
import pathlib
import srt
import re
import numpy as np
import mplcursors
import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib.widgets import Button, Slider
import xml.etree.ElementTree as ET



# in the SRT files, data for each frame is separated by blank lines and begins
# 1
# 00:00:00,000 --> 00:00:00,033
# <font size="36">FrameCnt : 1, DiffTime : 33ms
# 2024-09-30 13:36:16,091,732
# [iso : 100] [shutter : 1/240.0] [fnum : 900] [ev : 0] [ct : 5502] [color_md : default] [focal_len : 280] [latitude : 38.904608] [longtitude : -92.281470] [altitude: 260.226990] </font>
#
# 2
# etc
#
# in the second line iine of the frame's SRT entry, the first time is the
# elapsed time from the beginning of the video.  So fancy parsing of the
# datetime is unnecessary.
#
# Fluharty and Kazic, 29.1.2026


def parse_subtitles(contents):
    subs = srt.parse(contents)
 
    parsed = []
    for sub in subs:
        xml_root = ET.fromstring(sub.content)
        visible_text = xml_root.text


# this is extraneous
#
# assume last six digits are really microseconds        
# ['2024-09-30 13:38:24,653,570']
#
#         timestampish = re.findall(r'(\d{4}\-\d{2}\-\d{1,2}\s[\d{1,2}\:\d{1,2}\:\d{1,2}\:[\d\,]+)',visible_text)
#         timeish = str(timestampish).replace(",",".",1)
#         timestamp = re.sub(r',','',timeish)
#
#        timestamp_obj = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
#
# Kazic, 29.1.2026

        kv_pairs = re.findall(r'([^\s\[]+) ?: ([^\s,\]]+)', visible_text)
        kv_map = dict(kv_pairs)
        print("-" * 20)
        print(visible_text)        
        print(timestamp_obj)        
        print(kv_map)        
        parsed.append({
            'frame_number': int(kv_map['FrameCnt']), # just to make sure we match
            'timestamp': float(kv_map['altitude']),            
            'longitude': float(kv_map['longtitude']),
            'latitude': float(kv_map['latitude']),
            'altitude': float(kv_map['altitude'])            
        })
       
    return parsed


# This script processes SRT files in a given directory, generates flight path graphs, and saves them as PNG files.
# It also writes the filepaths of the generated graphs to a CSV file.


def process_video_data(file_path):

#    print(f"bar {type(file_path)}")
    
#    Check if file exists and read it---------------------------------
    try:
        content_string = file_path.read_text() # Get text from SRT

        if len(content_string) == 0:
            return
        
        filename_root = file_path.stem # Get DJI_0###

        # Get parts of file path as a tuple (for table labeling)
        file_name_parts = file_path.parts
        meaningful_parent_partial_path =  file_name_parts[5] + '/' + file_name_parts[6] + '/' + file_name_parts[7] + '/' + filename_root + '.MOV'

    except FileNotFoundError:
        print(f"File {file_path} not found.")


#    extract telemetry---------------------------------------------------------------

# create a single dataframe for each SRT file, appending the parsing output to that frame


#     subtitle_generator = srt.parse(content_string)
#     subtitles = list(subtitle_generator)
# 
#     for sub in subtitles:
#         print(f"Index: {sub.index}")
#         print(f"Content: {sub.content}")
# #        pattern = re.compile(r"rameCnt\s*\:\s*(\d+)[\s\w\,\:\-\n\r\[\/\_\]\.]*\[latitude\s:\s]([\d\.]+)\]",flags=re.MULTILINE) #\s*\[longt?itude\s*:\s*([-?\d.]+)\]\s*\[altitude:\s*([-?\d.]+)\]",flags=re.IGNORECASE)
#         pattern = re.compile(r"rameCnt\s*\:\s*(\d+).+\[latitude\s:\s]([\d\.]+)\]",flags=re.MULTILINE) # \[latitude\s:\s([\d\.]+)\]",flags=re.MULTILINE) #\s*\[longt?itude\s*:\s*([-?\d.]+)\]\s*\[altitude:\s*([-?\d.]+)\]",flags=re.IGNORECASE)
#         matches = pattern.findall(sub.content)
#         print(matches)        
# #        data = [{'frame':int(cnt), 'latitude': float(lat), 'longtitude': float(lon), 'altitude': float(alt)} for cnt, lat, lon, alt in matches]
#         data = [{'frame':int(cnt),'latitude':float(lat)} for cnt, lat in matches]
#         print(data)        
#         print("-" * 20)

    subtitles = parse_subtitles(content_string)
#    print('subs:', subtitles)
