#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import base64, email.parser, email.Header, datetime, imaplib, ConfigParser, re, sys


# Show help message
def showHelp():
	print "Simple mail checker\n"
	print "Command line arguments:"
	print "\thelp\t- show this message"
	print "\tcheck\t- check config file"
	print "\tfer\t- check FER webmail for new emails"
	exit()

# Print parsed values from config file
def checkConfig(Config, section):
	try:
		print "Section '", section, "':"
		print "\tAddress: ", Config.get(section, "Address")
		print "\tPort: ", Config.get(section, "Port")
		print "\tAuth: ", Config.get(section, "Auth")
		print "\tUsername: ", Config.get(section, "Username")
		print "\tPassword: ", Config.get(section, "Password"), "(base64 encoded)\n"
	except:
		print "\tERR: Section '" + section + "' in config file is incorrect.\n"

# Retrieve and show unread mails
def retrieve(Config, domain):
	# Connect
	hostname = Config.get(domain, "Address")
	print "Connecting to", hostname
	connection = imaplib.IMAP4_SSL(hostname)

	# Login
	username = Config.get(domain, 'Username')
	password = base64.b64decode(Config.get(domain, 'Password'))
	print "Logging in as", username
	connection.login(username, password)

	# Show number of unread messages
	(returnCode, unread) = connection.status("INBOX", "UNSEEN")
	if returnCode == "OK":
		print "\n", domain, ": Unread messages:", re.search("\d+", unread[0]).group(0)
		print '-' * 80
	else:
		print "\n", domain, ": Error while getting messages."

	# Fetch unread messages and show DATE, FROM, SUBJECT
	connection.select("INBOX")
	typ, data = connection.search(None, "UNSEEN")
	mailIDs = data[0].split()

	for i in mailIDs[::-1]:
		typ, data = connection.fetch(i, "(BODY.PEEK[HEADER])")

		for responsePart in data:
			if isinstance(responsePart, tuple):
				msg = email.message_from_string(responsePart[1])
				mDateRaw = msg['date']
				mDate = datetime.datetime.strptime(mDateRaw, "%a, %d %b %Y %H:%M:%S +0200")
				realDate = datetime.date.strftime(mDate, "%d.%m.%y, %H:%M")
				mFrom = msg['from']
				mSubject = msg['subject']
				realSubject, encoding = email.Header.decode_header(mSubject)[0]

		print realDate, "|", mFrom
		print "Subj:", realSubject, "\n"

	# Logout
	print "\nLogging out..."
	connection.close()
	connection.logout()



Config = ConfigParser.ConfigParser()
Config.read("./config.ini")

if "check" in sys.argv:
	checkConfig(Config, "webmail@fer.hr")
	exit()
elif "help" in sys.argv:
	showHelp()
	exit()
else:
	retrieve(Config, "webmail@fer.hr")