#!/bin/bash

# Configuration
source_dir="/path/to/local/images"          # Local directory containing the images
nextcloud_server="your.nextcloud.server"    # Nextcloud server address
nextcloud_user="your_nextcloud_user"        # Nextcloud username
nextcloud_dir="remote_path/on/nextcloud"    # Remote path on Nextcloud

# Function to recursively copy files and directories
recursive_copy() {
  local source="$1"
  local destination="$2"

  for item in "$source"/*; do
    if [ -d "$item" ]; then
      local dir_name=$(basename "$item")
      sshpass -p "$nextcloud_password" scp -r "$item" "$nextcloud_user@$nextcloud_server:$destination/$dir_name"
      recursive_copy "$item" "$destination/$dir_name"
    elif [ -f "$item" ]; then
      sshpass -p "$nextcloud_password" scp "$item" "$nextcloud_user@$nextcloud_server:$destination"
    fi
  done
}

# Prompt for Nextcloud password
echo -n "Enter your Nextcloud password: "
read -s nextcloud_password
echo

# Check if the source directory exists
if [ ! -d "$source_dir" ]; then
  echo "Source directory not found: $source_dir"
  exit 1
fi

# Copy the directory to Nextcloud
sshpass -p "$nextcloud_password" scp -r "$source_dir" "$nextcloud_user@$nextcloud_server:$nextcloud_dir"
recursive_copy "$source_dir" "$nextcloud_dir"

# Cleanup
unset nextcloud_password

echo "Copy completed."
