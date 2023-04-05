import os
import csv
import hashlib
import time
import argparse

#######################
###### ARGUMENTS ######
#######################

parser = argparse.ArgumentParser(
	description ="Script to check the files with same name and different file tpye, Mar 2023")

parser.add_argument(
        '-d','--dir', type=str,
        help='Targed directory, e.g. /home/test/targeted_directory', required=True)
parser.add_argument(
        '-l','--logdir', type=str,
        help='Projectlog output directory, e.g. /home/test/output/', required=False)

parser.add_argument(
        '-c','--csvname', type=str,
        help='Projectlog csv name, e.g. 1509.csv ', required=False)

parser.add_argument(
        '-e','--ext', nargs="+", type=str,
        help='Targeted extensions, e.g. .iso .tiff', required=False)

## Array for all args passed to script
args = parser.parse_args()

###############################
########## VARIABLES ##########
###############################

directory = args.dir

if args.logdir:
	logdirectory = args.logdir
else:
	logdirectory = ""

if args.csvname:
	csvname = args.csvname
else:
	csvname = "file-list.csv"


targed_ext = tuple(args.ext)


# Create a dictionary to store the file types and their respective file names
file_dict = {}

# Loop through the targed files in the directory and group them by file type
for file in [f for f in os.listdir(directory) if f.endswith(targed_ext)]:
    # Do something with the file:
    # Split the file name and extension
    name, ext = os.path.splitext(file)
    # Add the file name to the list of the corresponding file type in the dictionary
    if ext in file_dict:
        file_dict[ext].append(name)
    else:
        file_dict[ext] = [name]

# Write the file names and types to a CSV file, sorted by file type
with open(str(logdirectory) + "/" + str(csvname), "w", newline="") as file:
    writer = csv.writer(file)
    # Write the headers for the columns
    headers = ["File_name"]
    for ext in sorted(file_dict.keys()):
        if ext in targed_ext:
            headers.append(ext)
    headers.append("iso_md5-checksum")
    headers.append("iso_modification_time")
    writer.writerow(headers)
    # Write each file type, iso file md5 checksum and modification time to rows
    for name in sorted(set([name for names in file_dict.values() for name in names])):
        row = [name]
        for ext in sorted(file_dict.keys()):
            # For file type(s)
            if ext in targed_ext:
                if name in file_dict[ext]:
                    row.append(name+ext)
                else:
                    row.append("")
        # For iso files md5 checksum & modification time
        if name in file_dict[ext]:
            iso_file_path = str(directory) + "/" + str(name) + ".iso" # Define iso file path
            try:
                modification_time = str(time.ctime(os.path.getmtime(iso_file_path))) # Get modification time of iso file
                with open(iso_file_path, 'rb') as file:
                    md5_hash = hashlib.md5()
                    chunk = 0
                    while chunk != b'':
                        chunk = file.read(1024)
                        md5_hash.update(chunk)
                md5_checksum = md5_hash.hexdigest()
                row.append(md5_checksum) # Add the iso file checksum to the row
                row.append(modification_time) # Add the iso file modfication time to the row
            except:
                pass
        else:
            row.append("")
        writer.writerow(row)
