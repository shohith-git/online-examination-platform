#!/bin/bash

# -------------------------------------------------------
# EC2 User Data Script
# Project: Highly Available Three-Tier Online Examination Platform
# Description: Automatically configures an EC2 instance to
# deploy the Flask application using Gunicorn.
# -------------------------------------------------------

# Update system packages
dnf update -y

# Install required packages
dnf install -y git python3 python3-pip

# Navigate to the EC2 user's home directory
cd /home/ec2-user

# Clone the GitHub repository
git clone https://github.com/shohith-git/online-examination-platform.git

# Navigate into the project directory
cd online-examination-platform

# Create a Python virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt

# Create the environment configuration file
cat <<EOF > /home/ec2-user/online-examination-platform/.env
DB_HOST=<RDS_ENDPOINT>
DB_USER=<DB_USERNAME>
DB_PASSWORD=<DB_PASSWORD>
DB_NAME=<DATABASE_NAME>
EOF

# Create the systemd service for Gunicorn
cat <<EOF > /etc/systemd/system/exam.service
[Unit]
Description=Online Examination Platform
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/home/ec2-user/online-examination-platform
Environment="PATH=/home/ec2-user/online-examination-platform/venv/bin"
ExecStart=/home/ec2-user/online-examination-platform/venv/bin/gunicorn --workers 2 --bind 0.0.0.0:5000 app:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd configuration
systemctl daemon-reload

# Enable the application service
systemctl enable exam

# Start the application service
systemctl start exam
