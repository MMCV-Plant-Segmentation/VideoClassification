# this is /deltos/e/pointillist_maize/code/video_classification/flightpathonefile.py
#
# Evie Wilbur, spring, 2025

import sys
import pathlib
import re
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# This script processes SRT files in a given directory, generates flight path graphs, and saves them as PNG files.
# It also writes the filepaths of the generated graphs to a CSV file.
def process_video_data(file_path, output_directory, add_to_list=True):
    try:
        content_string = file_path.read_text() # Get text from SRT

        if len(content_string) == 0:
            return
        
        filename_root = file_path.stem # Get DJI_0###

        # Get parts of file path as a tuple (for table labeling)
        file_name_parts = file_path.parts
        meaningful_parent_partial_path =  file_name_parts[5] + '/' + file_name_parts[6] + '/' + file_name_parts[7] + '/' + filename_root + '.MOV'


        
#        print(f"foo {type(filename_root)}")
    except FileNotFoundError:
        print(f"File {file_path} not found.")


#    extract telemetry---------------------------------------------------------------
    pattern = re.compile(r"\[.*?latitude\s*:\s*([-\d.]+)\]\s*\[longtitude\s*:\s*([-\d.]+)\]\s*\[altitude:\s*([-\d.]+)\]",
        re.IGNORECASE)

    matches = pattern.findall(content_string)

#    convert matches---------------------------------------------------------------------------
    data = [{'latitude': float(lat), 'longtitude': float(lon), 'altitude': float(alt)} for lat, lon, alt in matches]
    df = pd.DataFrame(data)

#    max altitude--------------------------------------------------------------------------------
    max_altitude = df['altitude'].max()
    print(f"Max altitude: {max_altitude}")


#    plot flight path ----------------------------------------------------------------------------
    plt.figure(figsize=(8, 6))
    plt.plot(df['longtitude'], df['latitude'], marker='o', linestyle='-')
    plt.title(f"Flight Path {filename_root} (Latitude vs Longitude)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.text(x=1, y=1, s=f'Max altitude = {max_altitude}', verticalalignment='top', horizontalalignment='right', fontstyle='italic', fontsize='medium', transform=plt.gca().transAxes)
    plt.grid(True)
    plt.tight_layout()


#    save plot to file----------------------------------------------------
    new_file_path = (output_directory/filename_root).with_suffix('.png')
#    print(f"output is {new_file_path}")

    plt.savefig(new_file_path, dpi=300)

    #close plot
    plt.close()

    if not add_to_list:
        return

#   write video info to org table-----------------------------------------------
    org_file_path = "/deltos/f/aerial_imaging/lat_long_plots/all_flight_paths.org" 
    mov_file_path = file_path.with_suffix(".MOV")
    print(mov_file_path) 
  
    if  pathlib.Path(org_file_path).exists(): # check if the org file exists
        with open(org_file_path, 'a') as org_file:
            org_file.write(f"|[[{mov_file_path}][{meaningful_parent_partial_path}]]|[[{new_file_path}][plot]]|{max_altitude}||\n")

    else: # if not, create it
        print("org file not found, creating a new one at # this is /deltos/f/aerial_imaging/lat_long_plots/all_flight_paths.org...")

        with open(org_file_path, 'a') as org_file:
            org_file.write("# this is /deltos/f/aerial_imaging/lat_long_plots/all_flight_paths.org\n\n")
            org_file.write("| video                        | plot | max altitude | comments |\n|------------------------------+------+--------------+----------|\n|  |  |              |          |\n")
            org_file.write(f"|[[{mov_file_path}][{meaningful_parent_partial_path}]]|[[{new_file_path}][plot]]|{max_altitude}||\n")

        

    

#   CSV file of paths of processed videos------------------------------
    csv_file_path = "/deltos/f/aerial_imaging/lat_long_plots/all_flight_paths.csv"
    
    if  pathlib.Path(csv_file_path).exists(): # check if the CSV file exists
        with open(csv_file_path, 'a') as csv_file:
            csv_file.write(f"{file_path},\n")
    else:
        print("CSV file not found.")


