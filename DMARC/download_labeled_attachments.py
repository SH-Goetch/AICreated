import subprocess
import os
import zipfile
import gzip
import shutil

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
extract_folder = '/path/to/extracted/files'  # Replace with your desired extraction folder

# Function to extract zip file
def extract_zip(zip_file, extract_to):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

# Function to extract gzip file
def extract_gzip(gzip_file, extract_to):
    with gzip.open(gzip_file, 'rb') as f_in:
        with open(extract_to, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

# Command to list messages with attachments under a specific label and save attachments
list_messages_cmd = f"{GAM_PATH} user {EMAIL} show messages matchlabel {LABEL_MATCH} showattachments saveattachments targetfolder {TARGET_FOLDER} overwrite false"

# Execute the command
subprocess.run(list_messages_cmd, shell=True)

# Process downloaded attachments
for root, dirs, files in os.walk(TARGET_FOLDER):
    for file in files:
        file_path = os.path.join(root, file)
        if file.endswith('.zip'):
            # Create a directory for extracted contents
            os.makedirs(extract_folder, exist_ok=True)
            # Extract zip file contents to extract_folder
            extract_zip(file_path, extract_folder)
        elif file.endswith('.gz'):
            # Create a directory for extracted contents (assuming single file in gzip)
            os.makedirs(extract_folder, exist_ok=True)
            # Extract gzip file contents to extract_folder
            extract_gzip(file_path, os.path.join(extract_folder, os.path.basename(file_path)[:-3]))
