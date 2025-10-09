# this is /deltos/e/pointillist_maize/code/video_classification/getplotsfromvids.py
#
# Evie Wilbur, spring, 2025

import sys
import os
import pathlib
import creategraphsfordirectory as creategraphs


'''This script...
1. Takes an input directory and an output directory as command-line arguments.
2. Validates the input directory and creates the output directory if it doesn't exist.
3. Calls the create_graphs_for_directory function to process SRT files in the input directory and generate flight path graphs.'''


# looks like it wants /deltos/f/aerial_imaging/images/CROP/grace/SUBDIR for input and
# /deltos/f/aerial_imaging/lat_long_plots/CROP/ for output
#
# assumption is we're only interested in grace's flights
# code does not appear to descend directory tree
#
# calling order of scripts is:  getplotsfromvids.py (this one)
#                               creategraphsfordirectory.py
#                               flightpathonefile.py
#
# Kazic, 18.9.2025



# Get command-line arguments
if len(sys.argv) != 3:
    print("Usage: python creategraphsfordirectory.py <input_directory> <output_directory>")
    sys.exit(1)

# Set input and output directories
input_directory = sys.argv[1]
output_directory = sys.argv[2]


# print(f"command line input for creategraphsfordirectory.py is {input_directory} and output is {output_directory}")

# Validate input directory
if not os.path.isdir(input_directory):
    print(f"Error: Input directory '{input_directory}' does not exist.")
    sys.exit(1)

# Create output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

input_directory = pathlib.Path(input_directory)
output_directory = pathlib.Path(output_directory)


# Call create_graphs_for_directory function to process files
creategraphs.create_graphs_for_directory(input_directory, output_directory)

# print(f"creategraphsfordirectory.py computed plots from {input_directory} and put the output in {output_directory}")
