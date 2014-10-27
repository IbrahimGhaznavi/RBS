import sys
import re
from freeswitch import *
from libvbts import Database
import logging


ParentDbPath="/var/lib/asterisk/sqlite3dir/sqlite3.db"

def usage():
    res = "VBTS_GetDialStrings:\n" + "VBTS_GetDialStrings attribute|value\n"
    return res


def parse(args):
    res = args.split("|")
    if (len(res) < 2):
        return (None, None)
    return (res[0], res[1])

def GetDoctors(args):
	(attribute, value) = parse(args)
	consoleLog('info', "Got Args: " + str(args) + "\n")
	consoleLog('info', "Using sqlite:" + str(Database.using_sqlite3) + " Version:" + str(Database.sqlite_version) + "\n")
	logging.basicConfig(filename="/tmp/VBTS.log", level="DEBUG")
	if (attribute == None or value == None):
		return None
	con = Database.connect(str(ParentDbPath))
	cur = con.cursor()
	query = "SELECT name,ipaddr,port FROM sip_buddies WHERE " + attribute + " LIKE '%" + value + "%'"
	cur.execute(query)
	rows = cur.fetchall()
	masterstring=''
	for row in rows:
		row = "sofia/internal/" + row[0] + "@" + row[1] + ":" + row[2] + "|"
		masterstring += '%s' %row

	if not(masterstring):
		return "No record found"

	masterstring = masterstring[:-1]
	return masterstring

def fsapi(session, stream, env, args):
	res = str(GetDoctors(args))
	if(res):
		consoleLog('info', "Returned Dialstrings: " + res + "\n")
		stream.write(res)
	else:
		consoleLog('info', "Usage: " + usage() + "\n")
		stream.write(usage())

