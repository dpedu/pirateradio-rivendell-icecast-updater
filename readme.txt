udpupdate.py

a utility to update icecast2 metadata from Rivendells RDAirplay application

Rivendell needs to be configured to send now & next parameters to 127.0.0.1:9999
Configuration section: RDadmin-Hosts-Your Host-RDAirPlay-Now and Next:
Data Format: %a --- %t

configuation options (found in script)
ICECAST_ADMIN_URL: URL to icecast admin interface (usually http://myicecasthost:8000/admin)
ICECAST_ADMIN_USER: admin username
ICECAST_ADMIN_PASSWORD: admin password
MOUNTS: python List of mounts this script will update
DEFAULT_MESSAGE: message shown if no metadata is present
LISTEN_PORT: port to listen for meta updates