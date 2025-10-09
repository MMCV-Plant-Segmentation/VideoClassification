# this is /deltos/e/pointillist_maize/code/video_classification/creategraphsfordirectory.py
#
# Evie Wilbur, spring, 2025

import sys
import os
import flightpathonefile as flightpath

# This script processes SRT files in a given directory, generates flight path graphs, and saves them as PNG files.
def create_graphs_for_directory(input_directory, output_directory):

    # Process each SRT file in the input directory
    for files in os.listdir(input_directory):
#        print(type(input_directory/files))
#        if files.endswith('.png'):
        if files.endswith('.SRT'):        
            flightpath.process_video_data(input_directory/files, output_directory)
            # Move the generated PNG file to the output directory
#            os.rename(input_directory/files, output_directory/files)
