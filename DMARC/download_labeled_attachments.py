import subprocess
import os

# Path to GAM executable
GAM_PATH = '/path/to/gam'

# Specify the GAM configuration directory
GAM_CONFIG_DIRECTORY = '/path/to/.gam'

# Ensure GAM_CONFIG_DIRECTORY is set in the environment
os.environ['GAM_CONFIG_DIRECTORY'] = GAM_CONFIG_DIRECTORY

# Email and label information
EMAIL = 'your-email@example.com'
LABEL_NAME = 'your-label-name'

# Command to list messages with attachments
list_messages_cmd = f"{GAM_PATH} user {EMAIL} show messages query 'label:{LABEL_NAME} has:attachment'"

# Command to get downloaded message IDs
get_downloaded_messages_cmd = "cat downloaded_messages.txt"  # Adjust as per your storage method

# Execute commands
proc_list_messages = subprocess.Popen(list_messages_cmd, shell=True, stdout=subprocess.PIPE)
proc_get_downloaded = subprocess.Popen(get_downloaded_messages_cmd, shell=True, stdout=subprocess.PIPE)

# Read message IDs from commands output
current_messages = proc_list_messages.stdout.read().decode('utf-8').strip().split('\n')
downloaded_messages = proc_get_downloaded.stdout.read().decode('utf-8').strip().split('\n')

# Filter out already downloaded message IDs
new_messages = [msg_id for msg_id in current_messages if msg_id not in downloaded_messages]

# Download attachments for new messages
for msg_id in new_messages:
    download_attachments_cmd = f"{GAM_PATH} user {EMAIL} get message {msg_id} parts targetfolder attachments"
    subprocess.run(download_attachments_cmd, shell=True)
    
    # Record downloaded message ID
    with open('downloaded_messages.txt', 'a') as f:
        f.write(msg_id + '\n')
