import os
import sys
import re
def sort_key(filename):
    numeric_prefix = re.findall('\d+', filename)
    numeric_value = int(numeric_prefix[0])
    return (numeric_value, filename)


# Parse the command-line arguments
if len(sys.argv) != 5:
    print("Usage: python upgrade_db.py your_username host db_name your_password")
    sys.exit(1)

username = sys.argv[1]
host = sys.argv[2]
db_name = sys.argv[3]
password = sys.argv[4]

# Set directory to read upgrade scripts from
script_dir = 'scripts/'


# Get a list of all the SQL script files in the scripts directory
dir_files = os.listdir(script_dir)
script_files = []

# Select only .sql files that contain digits
for file in dir_files:
    if file.endswith('.sql'):
        if file[:1].isdigit():
            script_files.append(file)

# Sort the files by their numeric prefix, then by their filename
script_files.sort(key=sort_key)

# Execute the scripts that have a higher version number than the current version
for script_file in script_files:
    print(script_file)


