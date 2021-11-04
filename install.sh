#!/bin/bash

# Install pip packages
apt install -y python3 python3-pip

# Install gitlab module
pip3 install -r requirements.txt

# Create systemd service file
cat << EOF >> /usr/lib/systemd/system/gitbot.service
[Unit]
Description=gitBot Endpoint
After=syslog.target
[Service]
LimitNOFILE=65536
ExecStart=/usr/bin/python3 /opt/gitbot/gitbot.py -c /opt/gitbot/gitbot.conf 
RestartSec=5s
Restart=on-success
[Install]
WantedBy=multi-user.target
EOF

# Reload daemon
systemctl daemon-reload 
systemctl start gitbot.service
systemctl enable gitbot.service