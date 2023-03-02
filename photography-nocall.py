import sys
import argparse 
import os
import subprocess as subproc
import datetime
import re

#######################
###### ARGUMENTS ######
#######################

parser = argparse.ArgumentParser(
	description ="Script to walk through the photography workflow, Feb 2022")
parser.add_argument(
	'-c', '--collection', type=str,
	help='collection/accession/box/whatever', 
	required=True)
parser.add_argument(
        '-d','--dir', type=str,
        help='Start directory, e.g. /home/jess/CAPTURED', required=True)
parser.add_argument(
	'-n','--note', type=str,
	help='capture notes', required=False)
parser.add_argument(
	'-k', '--key',type=str,
	help='photoIDID',required=True)

## Array for all args passed to script
args = parser.parse_args()

###############################
########## VARIABLES ##########
###############################

date = datetime.datetime.today().strftime('%Y-%m-%d')
collection = args.collection
key = args.key
dir = args.dir
note=args.note
yes_string = ["y", "yes", "Yes", "YES"]
no_string = ["n", "no", "No", "NO"]

#################################
########## CLASS STUFF ##########
#################################

# font colors, visit https://gist.github.com/vratiu/9780109 for a nice guide to the color codes
class bcolors:
    OKGREEN = '\033[92m' #green
    INPUT = '\033[93m' #yellow, used for when user input required
    FAIL = '\033[91m' #red, used for failure
    ENDC = '\033[0m' # end color
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    GREENBLOCK = '\x1b[1;31;40m' # green with background, used for updates user should check (e.g. Title/Cat report)
    ENDGB = '\x1b[0m' #end x1b block

########################
#####  THE GOODS  ######
########################

### Change working directory
if not os.path.exists(dir):
	os.makedirs(dir)
	
os.chdir(dir)

### Create directory for output if it doesn't exist
outputPath = collection+"/"

### Change output directory
if not os.path.exists(outputPath):
	os.makedirs(outputPath)

###############################
########## CAMERA ##########
###############################

picName = key + ".jpg"
PicPath = outputPath + picName
picParameters = " --wait-event=1s --set-config eosremoterelease='Press 1' --wait-event=1s --set-config eosremoterelease='Press 2' --wait-event=100ms --set-config eosremoterelease='Release 2' --set-config eosremoterelease='Release 1' --wait-event-and-download=5s  --filename "+outputPath+picName+" --force-overwrite " + "> /dev/null" #Force overwrite the image file, and slient the output of the photo taking script by gphoto2 in the terminal. Updated in Jan 2023


## Modified version based on Dec 2022 to fit in the new picParameters. Updated in Jan 2023
if os.path.exists(PicPath):
	replacephotopath = input(bcolors.INPUT+"photo already exists, proceed anyway? [y/n]"+bcolors.ENDC)
	if replacephotopath not in no_string:
		gopic = input(bcolors.INPUT+"Please place disk for picture and hit Enter"+bcolors.ENDC)
		print("Wait please...taking picture...")
		os.system("gphoto2"+picParameters) #gphoto2 command
		if os.path.exists(PicPath):
			print("-Pic: %s is captured" % (PicPath))
	else:
		print("No photo is taken/modified")
else:
	gopic = input(bcolors.INPUT+"Please place the item for picture and hit Enter"+bcolors.ENDC)
	print("Wait please...taking picture...")
	os.system("gphoto2"+picParameters) #gphoto2 command
	if os.path.exists(PicPath):
		print("-Pic: %s is captured" % (PicPath))


#########################################
#### END MATTER and METADATA UPDATES ####
#########################################
### Update master log

## User asked if they'd like to update the notes they entered
noteupdate = input(bcolors.INPUT+"If you would like to update the notes (currently: "+bcolors.OKGREEN+str(note)+bcolors.ENDC+bcolors.INPUT+"), please re-enter, otherwise hit Enter: "+bcolors.ENDC)
if noteupdate:
	note = noteupdate
	print("-Note has been updated to: " + bcolors.OKGREEN + str(note) + bcolors.ENDC)
else:
	note = "No-notes"
	print("-Note unchanged...")
	
## Open and update the masterlog - projectlog.csv
log = open('projectlog.csv','a+')
print("-Updating log...")

log.write(
	"\n"+collection+","+key+",\""+str(note)+"\"")
if os.path.exists(
	outputPath+picName):
	log.write(",photo=OK")
else:
	log.write(",photo=NO")
log.write(","+date)

### Close master log
log.close()

sys.exit ()