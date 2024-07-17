import subprocess
import os

# Path to GAMADV-XTD3 executable
GAM_PATH = '/path/to/gamadv-xtd3/gam'

# Specify the GAM configuration directory
GAM_CONFIG_DIRECTORY = '/path/to/.gam'

# Ensure GAM_CONFIG_DIRECTORY is set in the environment
os.environ['GAM_CONFIG_DIRECTORY'] = GAM_CONFIG_DIRECTORY

# Email and label information
EMAIL = 'your-email@example.com'
LABEL_NAME = 'your-label-name'

# Target folder to save attachments
TARGET_FOLDER = '/path/to/save/attachments'  # Replace with your desired target folder

# Command to list messages with attachments
list_messages_cmd = f"{GAM_PATH} user {EMAIL} show messages query 'label:{LABEL_NAME} has:attachment'"

# Execute list messages command and capture output
proc_list_messages = subprocess.Popen(list_messages_cmd, shell=True, stdout=subprocess.PIPE)
list_messages_output = proc_list_messages.stdout.read().decode('utf-8').strip()

# Process each message ID
for msg_id in list_messages_output.splitlines():
    # Download attachments for each message
    download_attachments_cmd = f"{GAM_PATH} user {EMAIL} show message {msg_id} saveattachments targetfolder {TARGET_FOLDER}"
    subprocess.run(download_attachments_cmd, shell=True)
    
    # Record downloaded message ID (optional)
    with open('downloaded_messages.txt', 'a') as f:
        f.write(msg_id + '\n')
