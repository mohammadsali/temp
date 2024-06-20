#!/bin/bash

# Set variables
DIRECTORY="/etc/opt/BESClient"
FILE_SRC="/path/to/actionsite.afxm"  # Update this path to the location of your actionsite.afxm file
FILE_DEST="/etc/opt/BESClient/actionsite.afxm"
RPM_PACKAGE="/path/to/BESAgent-rhel7.rpm"  # Update this path to the location of your RPM package

# Create the directory with the specified permissions and ownership
echo "Creating directory: $DIRECTORY"
sudo mkdir -p $DIRECTORY
sudo chown root:root $DIRECTORY
sudo chmod 775 $DIRECTORY

# Copy the actionsite.afxm file to the directory
echo "Copying $FILE_SRC to $FILE_DEST"
sudo cp $FILE_SRC $FILE_DEST
sudo chown root:root $FILE_DEST
sudo chmod 644 $FILE_DEST

# Install the BigFix client
echo "Installing BigFix client from $RPM_PACKAGE"
sudo rpm -ivh $RPM_PACKAGE

echo "Setup completed successfully."
