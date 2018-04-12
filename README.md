# Pritunl-mailer
The Pritunl mailer script sends an e-mail when a user connects to OpenVPN which was setup with Pritunl. 

### Prerequisites
```
Install: python -m pip install pymongo

Configure mongodb to send an alert when a new log entry is generated:
1. login mongo
2. use pritunl
3. db.runCommand({"convertToCapped": "servers_output", size: 19262})
```

### Installing
Create service file:
```
sudo nano /etc/systemd/system/Pritunl-mailer.service 
```

Edit file:
```
[Unit]
Description=Pritunl mailer script

[Service]
User=media
Group=media
Restart=always
ExecStart=/usr/bin/python /usr/share/Pritunl_mailer.py

[Install]
WantedBy=multi-user.target
```

Reload systemd:
```
systemctl daemon-reload
```

Start new service:
```
systemctl enable Pritunl-mailer
```
