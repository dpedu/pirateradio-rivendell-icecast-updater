#!/usr/bin/env python
import syslog
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import base64
import urllib
import urllib2

# Rivendell needs to be configured to send now & next parameters to 127.0.0.1:9999
# RDadmin-Hosts-Your Host-RDAirPlay-Now and Next:
# Format: %a --- %t

# URL of icecast2 admin interface
ICECAST_ADMIN_URL = 'http://127.0.0.1:8000/admin'
# Icecast2 username and password
ICECAST_ADMIN_USER = 'admin'
ICECAST_ADMIN_PASSWORD = 'admin' 
# List of mounts this script will update
MOUNTS = ['myStream', 'myStream2']
# Message to show if data is missing (IE, Non-music content or paused rivendell)
DEFAULT_MESSAGE = "WQQN-DB/Rochester, NY - Pirate Radio - <http://pirateradio.rit.edu> - New Rock That's Actually New! A service of the RIT Streaming Media Club"
# Port this script will listen on
LISTEN_PORT = 9999

def update_icecast(text, mounts):
	for mount in mounts:
		data = (
			("song", text),
			("mount", "/"+mount),
			("mode", "updinfo"),
			("charset", "UTF-8")
		)
		
		url = "%s/%s?%s" % (ICECAST_ADMIN_URL, "metadata.xsl", urllib.urlencode(data))
		req = urllib2.Request(url)
		base64string = base64.encodestring('%s:%s' % (ICECAST_ADMIN_USER,ICECAST_ADMIN_PASSWORD))[:-1]
		req.add_header("Authorization", "Basic %s" % base64string)
		handle = urllib2.urlopen(req)
		content =  handle.read()
		
		if "Metadata update successful" in content:
			syslog.syslog("Updated mount %s: %s" % (mount, text))
		else:
			syslog.syslog("Failed to update mount %s: %s" % (mount, text))
				
class UDPListener(DatagramProtocol):
	def datagramReceived(self, data, (host, port)):
		syslog.syslog("received %r from %s:%d" % (data, host, port))
		stripdata = data.split()
		
		end_of_artist = 0
		done = False;
		ARTIST=''
		SONG=''
		
		for i in range(0,len(stripdata)-1):
			if stripdata[i] == "---":
				done = True
				end_of_artist = i
			if not done:
				ARTIST += " "
				ARTIST += stripdata[i]
		for j in range(end_of_artist + 1, len(stripdata)):
			SONG += " "
			SONG+=stripdata[j]
		ARTIST=ARTIST[1:]
		SONG=SONG[1:]
		if SONG == "" or ARTIST == "" or SONG == " " or ARTIST == " ":
			update_icecast(DEFAULT_MESSAGE, MOUNTS)
		else:
			update_icecast(ARTIST + " - " + SONG, MOUNTS)

if __name__ == '__main__':
		syslog.syslog("Icecast UDP watcher started...")
		reactor.listenUDP(LISTEN_PORT, UDPListener())
		reactor.run()

