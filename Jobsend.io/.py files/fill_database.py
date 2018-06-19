import common
import datetime as dt
import logging
logging.basicConfig(filename="/var/log/daily_log",level=logging.DEBUG)
startTime = dt.datetime.now()
logging.debug(str(dt.datetime.now()))

print "\n\n\n\n\n%s"%(str(dt.date.today()))
print "TRUNCATING TABLES"
try:
	import clear_table
except Exception as e:
	logging.debug("Clear table failed")
	logging.debug(str(e))

print "FIRSTJOB"
try:
	import firstjob
except Exception as e:
	logging.debug("Firstjob failed")
	logging.debug(str(e))

print "CAREERBUILDER"
try:
	import careerbuilder
except Exception as e:
	logging.debug("Careerbuilder failed")
	logging.debug(str(e))

print "ENGINEERJOBS"
try:
	import engineerjobs
except Exception as e:
	logging.debug("Engineerjobs failed")
	logging.debug(str(e))

print "INDEED"
try:
	import indeed
except Exception as e:
	logging.debug("Indeed failed")
	logging.debug(str(e))

print "MONSTER"
try:
	import monster
except Exception as e:
	logging.debug("Monster failed")
	logging.debug(str(e))

print "EMAILER"
try:
	import emailer
except Exception as e:
	logging.debug("Emailer failed")
	logging.debug(str(e))

print "Completed in " + str(dt.datetime.now() - startTime)