#!/usr/bin/env python

'''
The goal of this script is to send an e-mail when a user connects to a VPN server setup by Pritunl.

Requirement:
python -m pip install pymongo

Configure mongodb to send an alert when a new log entry is generated:
1. login mongo
2. use pritunl
3. db.runCommand({"convertToCapped": "servers_output", size: 19262})
'''

from pymongo import MongoClient, CursorType
from datetime import datetime
import datetime
import pprint
import time
import re
import smtplib
import sys
import logging

gmail_user = ''
gmail_pwd = '' # onetime password
logfile = '/var/log/Pritunl_mailer.log'

def send_email(gmail_user, gmail_pwd, ip, user_id):

	currenttime = datetime.datetime.now()
	currenttime_pretty = currenttime.strftime("%H:%M %d-%m-%Y")
	
	FROM = 'sjosz2000@gmail.com'
	TO = 'jos@clephas.nl'
	SUBJECT = 'Pritunl: %s logt in' %ip
	TEXT = 'Pritunl: Er is ingelogd om %s vanaf IP adres %s en de user id is %s' % (currenttime_pretty, ip, user_id)

	message = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (FROM, TO, SUBJECT, TEXT)
	
	print message
	logging.info(message)
	
	try:
	
		server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
		server_ssl.ehlo()
		server_ssl.login(gmail_user, gmail_pwd)  
		server_ssl.sendmail(FROM, TO, message)
		server_ssl.close()
		
		print 'E-mail verzonden'
		logging.info('E-mail verzonden')
		
	except Exception as e: 
		print (e)
		logging.warning(e)

logging.basicConfig(filename=logfile,level=logging.DEBUG,format='%(asctime)s %(message)s')
client = MongoClient("mongodb://localhost:27017") 
db = client.pritunl 
currenttime = datetime.datetime.utcnow()
log = db.servers_output.find({'timestamp': {'$gte': currenttime } }, cursor_type = CursorType.TAILABLE_AWAIT )

while log.alive:

	try:
	
		for entry in log:
		
			for key, value in entry.iteritems():
			
				if key == 'output':		
					match_1 = re.search('(User connected).*(?:user_id=)(.*)', value)
					match_2 = re.search('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*(?:send_push)', value)

			if match_1:
				user_id = match_1.group(2)
			
			if match_2:
				ip = match_2.group(1)		
				send_email(gmail_user, gmail_pwd, ip, user_id)
		
	except StopIteration:
		time.sleep(1)

