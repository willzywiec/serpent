#!/usr/bin/env python3
"""
xsdir_replace.py - A script to process MCNP xsdir files for Serpent compatibility

This script:
1. Removes all lines containing the # symbol
2. Removes strings that match 'xdata/' and 'xmc/'
3. Removes the XX/XX/XXXX format date line before the 'directory' string
4. Prepends 'datapath=home/mobaxterm/serpent/Serpent2xsdata' to the first line

Usage: python xsdir_replace.py input_file
"""

import sys
import os
import re

def process_file(input_file):
    # Set output filename to xsdir_serpent (no extension)
    output_file = "xsdir_serpent"
    
    # Read input file
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    # Process the content
    processed_lines = []
    skip_next_directory_line = False
    
    for line in lines:
        # Skip lines containing #
        if '#' in line:
            continue
        
        # Remove 'xdata/' and 'xmc/' strings
        line = line.replace('xdata/', '')
        line = line.replace('xmc/', '')
        
        # Check for date pattern before 'directory'
        if 'directory' in line and not skip_next_directory_line:
            # Look at the previous line for date pattern XX/XX/XXXX
            if processed_lines and re.search(r'\d{2}/\d{2}/\d{4}', processed_lines[-1]):
                processed_lines.pop()  # Remove the date line
        
        processed_lines.append(line)
    
    # Prepend the datapath to the first line (if there are any lines)
    if processed_lines:
        processed_lines[0] = f"datapath=home/mobaxterm/serpent/Serpent2xsdata\n{processed_lines[0]}"
    
    # Write the processed content to the output file
    with open(output_file, 'w') as file:
        file.writelines(processed_lines)
    
    print(f"Processed file saved as: {output_file}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python xsdir_replace.py input_file")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    
    process_file(input_file)

if __name__ == "__main__":
    main()
