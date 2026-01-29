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
import srt
import re
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use("WebAgg")

import pyperclip

import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.widgets import Slider, Button


# in the SRT files, data for each frame is separated by blank lines and begins
# 1
# 00:00:00,000 --> 00:00:00,033
# <font size="36">FrameCnt : 1, DiffTime : 33ms
# 2024-09-30 13:36:16,091,732
# [iso : 100] [shutter : 1/240.0] [fnum : 900] [ev : 0] [ct : 5502] [color_md : default] [focal_len : 280] [latitude : 38.904608] [longtitude : -92.281470] [altitude: 260.226990] </font>
#
# 2
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

        kv_pairs = re.findall(r'([^\s\[]+) ?: ([^\s,\]]+)', visible_text)
        kv_map = dict(kv_pairs)
        parsed.append({
            'timestamp': str(sub.start),
            'frame_number': int(kv_map['FrameCnt']),
            'latitude': float(kv_map['latitude']),
            'longitude': float(kv_map['longtitude']),
            'altitude': float(kv_map['altitude'])            
        })
       
    return parsed


def plot_points(data):
    lons = [d['longitude'] for d in data]
    lats = [d['latitude'] for d in data]
    
    fig, ax = plt.subplots(figsize=(10, 7))
    plt.subplots_adjust(bottom=0.25)

    ax.scatter(lons, lats, color='blue', alpha=0.3, label='Path')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('GPS Data Viewer')
    ax.grid(True)

    highlight, = ax.plot([lons[0]], [lats[0]], 'ro', markersize=12, label='Selected')

    info_template = 'Index: {idx}\nFrame: {frame}\nLat: {lat:.6f}\nLon: {lon:.6f}\nTime: {time}'
    
    text_box = ax.text(
        0.05, 0.95, 
        "", # Start empty, update() will fill it
        transform=ax.transAxes, 
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
        fontfamily='monospace'
    )

    # --- UI Layout ---
    ax_prev   = plt.axes([0.05, 0.1, 0.06, 0.04])
    ax_slider = plt.axes([0.15, 0.1, 0.55, 0.04]) # Slightly narrowed to fit Copy button
    ax_next   = plt.axes([0.74, 0.1, 0.06, 0.04])
    ax_copy   = plt.axes([0.84, 0.1, 0.11, 0.04]) # New Copy Button Axes

    btn_prev = Button(ax_prev, '<')
    btn_next = Button(ax_next, '>')
    btn_copy = Button(ax_copy, 'Copy Text')
    
    slider = Slider(
        ax=ax_slider,
        label='Index ',
        valmin=0,
        valmax=len(data) - 1,
        valinit=0,
        valstep=1
    )

    def update(val):
        idx = int(slider.val)
        point = data[idx]
        
        highlight.set_data([lons[idx]], [lats[idx]])
        
        content = info_template.format(
            idx=idx, 
            frame=point['frame_number'], 
            lat=point['latitude'], 
            lon=point['longitude'],
            time=point.get('timestamp', 'N/A')
        )
        text_box.set_text(content)
        fig.canvas.draw_idle()

    # --- Copy Logic ---
    def copy_to_clipboard(event):
        # Get the current text from the bubble
        current_text = text_box.get_text()
        pyperclip.copy(current_text)
        print(f"copied text {current_text}")
        
    # --- Event Handlers ---
    slider.on_changed(update)

    def go_next(event):
        if slider.val < slider.valmax:
            slider.set_val(slider.val + 1)

    def go_prev(event):
        if slider.val > slider.valmin:
            slider.set_val(slider.val - 1)

    btn_next.on_clicked(go_next)
    btn_prev.on_clicked(go_prev)
    btn_copy.on_clicked(copy_to_clipboard)

    def on_key(event):
        if event.key == 'right':
            go_next(None)
        elif event.key == 'left':
            go_prev(None)
        elif event.key == 'c': # Added 'c' key shortcut for copy
            copy_to_clipboard(None)

    fig.canvas.mpl_connect('key_press_event', on_key)

    # Initialize the display
    update(0)
    
    plt.legend(loc='upper right')
    plt.show()


def plot_srt(file_path):
    try:
        content_string = file_path.read_text()

    except FileNotFoundError:
        print(f"File {file_path} not found.")
    
    points = parse_subtitles(content_string)
    plot_points(points)

if __name__ =='__main__':
    plot_srt(Path('/deltos/f/aerial_imaging/images/24r/grace/30.9/DJI_0309.SRT'))
