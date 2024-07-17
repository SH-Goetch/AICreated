import subprocess
import os

# Path to GAMADV-XTD3 executable
GAM_PATH = '/path/to/gamadv-xtd3/gam'

# Specify the GAM configuration directory
GAM_CONFIG_DIRECTORY = '/path/to/.gam'

# Ensure GAM_CONFIG_DIRECTORY is set in the environment
os.environ['GAM_CONFIG_DIRECTORY'] = GAM_CONFIG_DIRECTORY

# Email and label information (replace with your own)
EMAIL = 'your-email@example.com'
LABEL_MATCH = 'your-label-match'
TARGET_FOLDER = '/path/to/save/attachments'  # Replace with your desired target folder

# Command to list messages with attachments under a specific label and save attachments
list_messages_cmd = f"{GAM_PATH} user {EMAIL} show messages matchlabel {LABEL_NAME} showattachments saveattachments targetfolder {TARGET_FOLDER}"

# Execute the command
subprocess.run(list_messages_cmd, shell=True)
