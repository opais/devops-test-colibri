import os
import sys
import re
import mysql.connector

# TODO: This sort function will break if the filenames it gets don't contain digits
def sort_key(filename):
    numeric_prefix = re.findall('\d+', filename)
    numeric_value = int(numeric_prefix[0])
    return (numeric_value, filename)


# Parse the command-line arguments
if len(sys.argv) != 5:
    print("Usage: python upgrade_db.py your_username host db_name your_password")
    sys.exit(1)

# TODO: These inputs should be sanitised
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

# Connect to the database
db_config = {
  'user': username,
  'password': password,
  'host': host,
  'database': db_name,
  'raise_on_warnings': True
}
conn = mysql.connector.connect(**db_config)

# Get the current database version from the versionTable
cursor = conn.cursor()
cursor.execute('SELECT version FROM versionTable')
current_version = cursor.fetchone()[0]

# TODO: We should have some error handling and error messages, right now, if something isn't right the script will just fail
# Execute the scripts that have a higher version number than the current version
for script_file in script_files:
    script_version = re.findall('\d+', script_file)
    script_version = int(script_version[0])

    if script_version > current_version:
        with open(os.path.join(script_dir, script_file), 'r') as f:
            print(script_file)
            script = f.read()
            cursor.execute(script)
            current_version = script_version
            cursor.execute('UPDATE versionTable SET version = %s', (current_version,))
            conn.commit()

# Close the database connection
conn.close()

