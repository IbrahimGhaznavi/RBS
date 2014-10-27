import sys
import re
from freeswitch import *
from libvbts import Database
import logging


ParentDbPath="/var/lib/asterisk/sqlite3dir/sqlite3.db"

def usage():
    res = "Follow this format:\nSearch<space>Attribute<space>Value"
    return res


def parse(args):
    res = args.split(" ")
    if (len(res) < 3):
        return (None, None, None)
    return (res[0], res[1], res[2])

def Search(args):
	(command, attribute, value) = parse(args)
	consoleLog('info', "Got Args: " + str(args) + "\n")
	consoleLog('info', "Using sqlite:" + str(Database.using_sqlite3) + " Version:" + str(Database.sqlite_version) + "\n")
	logging.basicConfig(filename="/tmp/VBTS.log", level="DEBUG")
	if (attribute == None or value == None):
		return "Invalid"
	con = Database.connect(str(ParentDbPath))
	cur = con.cursor()
	query = "SELECT uname, callerid, " + attribute + " FROM sip_buddies WHERE " + attribute + " LIKE '%" + value + "%'"
	cur.execute(query)
	rows = cur.fetchall()

	header="Search results for " + attribute + ": " + value + "\n" + "Name-Number-" + attribute + "\n"
	masterstring = ''
	for row in rows:
		row = row[0] + "-" + row[1] + "-" + row[2] + "\n"
		masterstring += '%s' %row

	if not(masterstring):
		return header + "No record found"

	masterstring = masterstring[:-1]
	return header + masterstring

def fsapi(session, stream, env, args):
	res = str(Search(args))
	if(res != "Invalid"):
		consoleLog('info', "Search Result: " + res + "\n")
		stream.write(res)
	else:
		consoleLog('info', "Usage: " + usage() + "\n")
		stream.write(usage())

