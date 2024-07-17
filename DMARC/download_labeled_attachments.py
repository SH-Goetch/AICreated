import subprocess
import os

# Path to GAM executable
GAM_PATH = '/Users/goetchstone/bin/gamadv-xtd3/gam'

# Specify the GAM configuration directory
GAM_CONFIG_DIRECTORY = '/Users/goetchstone/GAMConfig'

# Ensure GAM_CONFIG_DIRECTORY is set in the environment
os.environ['GAM_CONFIG_DIRECTORY'] = GAM_CONFIG_DIRECTORY

# Email and label information
EMAIL = 'gstone@saybrookhome.com'
LABEL_MATCH = 'DMARC'
TARGET_FOLDER = '/Users/goetchstone/AICreated/DMARC/attachments/'

# Command to list messages with attachments under a specific label and save attachments without overwriting
list_messages_cmd = f"{GAM_PATH} user {EMAIL} show messages matchlabel {LABEL_MATCH} showattachments saveattachments targetfolder {TARGET_FOLDER} overwrite true"

# Execute the command
subprocess.run(list_messages_cmd, shell=True)
