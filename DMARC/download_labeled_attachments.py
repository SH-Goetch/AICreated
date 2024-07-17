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

# Regular expression pattern to match attachment names (optional)
ATTACHMENT_NAME_PATTERN = '.*'  # Match all attachments, change as needed

# Command to list messages with attachments under a specific label
list_messages_cmd = f"{GAM_PATH} user {EMAIL} show messages matchlabel {LABEL_NAME} showattachments"

# Execute list messages command and capture output
proc_list_messages = subprocess.Popen(list_messages_cmd, shell=True, stdout=subprocess.PIPE)
list_messages_output = proc_list_messages.stdout.read().decode('utf-8').strip()

# Process each message in the output
for line in list_messages_output.splitlines():
    if line.startswith('Message:'):
        msg_id = line.split()[1]  # Extract the message ID
        continue  # Skip to the next line
    
    # Extract attachment details
    if line.startswith('Attachment:'):
        attachment_info = line.split()
        attachment_name = attachment_info[1]  # Extract attachment name
        
        # Download attachment
        download_attachments_cmd = f"{GAM_PATH} user {EMAIL} show message {msg_id} saveattachments attachmentnamepattern '{ATTACHMENT_NAME_PATTERN}' targetfolder {TARGET_FOLDER}"
        subprocess.run(download_attachments_cmd, shell=True)
        
        # Record downloaded message and attachment (optional)
        with open('downloaded_attachments.txt', 'a') as f:
            f.write(f"Message ID: {msg_id}, Attachment: {attachment_name}\n")
