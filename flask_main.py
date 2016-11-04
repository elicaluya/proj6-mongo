"""
Flask web app connects to Mongo database.
Keep a simple list of dated memoranda.

Representation conventions for dates: 
   - We use Arrow objects when we want to manipulate dates, but for all
	 storage in database, in session or g objects, or anything else that
	 needs a text representation, we use ISO date strings.	These sort in the
	 order as arrow date objects, and they are easy to convert to and from
	 arrow date objects.  (For display on screen, we use the 'humanize' filter
	 below.) A time zone offset will 
   - User input/output is in local (to the server) time.  
"""

import flask
from flask import g
from flask import render_template
from flask import request
from flask import url_for

import json
import logging

# Date handling 
import arrow	# Replacement for datetime, based on moment.js
# import datetime # But we may still need time
from dateutil import tz	 # For interpreting local times

# Mongo database
from pymongo import MongoClient
import secrets.admin_secrets
import secrets.client_secrets
MONGO_CLIENT_URL = "mongodb://{}:{}@localhost:{}/{}".format(
	secrets.client_secrets.db_user,
	secrets.client_secrets.db_user_pw,
	secrets.admin_secrets.port, 
	secrets.client_secrets.db)

###
# Globals
###
import CONFIG
app = flask.Flask(__name__)
app.secret_key = CONFIG.secret_key

####
# Database connection per server process
###

try: 
	dbclient = MongoClient(MONGO_CLIENT_URL)
	db = getattr(dbclient, secrets.client_secrets.db)
	collection = db.dated

except:
	print("Failure opening database.  Is Mongo running? Correct password?")
	sys.exit(1)



###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
  app.logger.debug("Main page entry")
  g.memos = get_memos()
  for memo in g.memos: 
	  #app.logger.debug("Memo: " + str(memo))
	  pass
  return flask.render_template('index.html')


# We don't have an interface for creating memos yet
@app.route("/create")
def create():
	app.logger.debug("Create")
	return flask.render_template('create.html')


@app.errorhandler(404)
def page_not_found(error):
	app.logger.debug("Page not found")
	return flask.render_template('page_not_found.html',
								 badurl=request.base_url,
								 linkback=url_for("index")), 404

#################
#
# Functions used within the templates
#
#################

#Function for adding data into the memos database
@app.route("/add")
def add():
	date =""
	memo=""
	date = request.args.get("date" , type=str)
	app.logger.debug("date entered: {}".format(date))
	memo = request.args.get("memo", type=str)
	app.logger.debug("text entered: {}".format(memo))
	note = { "type": "dated_memo", 
           "date": date,
           "text": memo}
	added = collection.insert_one(note).inserted_id
	g.memos = get_memos()
	return flask.render_template('index.html')

#Function for deleting selected items from memos database
@app.route("/delete")
def delete():
	check = request.args.getlist('check', type = str)
	app.logger.debug("Delete function got checklist {}".format(check))
	for to_delete in check:
		app.logger.debug("Deleting memo on {}".format(to_delete))
		find = collection.find_one({"text": to_delete})
		app.logger.debug("found {}".format(find))
		delete = collection.delete_one({"_id": find['_id']})
		app.logger.debug("Deleted {} items".format(delete.deleted_count))
	g.memos = get_memos()
	return flask.render_template('index.html')

@app.template_filter( 'humanize' )
def humanize_arrow_date( date ):
	"""
	Date is internal UTC ISO format string.
	Output should be "today", "yesterday", "in 5 days", etc.
	Arrow will try to humanize down to the minute, so we
	need to catch 'today' as a special case. 
	"""
	try:
		then = arrow.get(date).to('local')
		now = arrow.utcnow().to('local')
		if then.date() == now.date():
			app.logger.debug("then date {}".format(then.date()))
			app.logger.debug("now date {}".format(now.date()))
			human = "Today"
		else: 
			replace = then.replace(days=+1)
			human = replace.humanize()
			
			if "in" in human and ("hours" in human or "minutes" in human):
				human = "Tomorrow"
			elif "ago" in human and ("hours" in human or "minutes" in human):
				human = "Yesterday"
	except: 
		human = date
	return human


#############
#
# Functions available to the page code above
#
##############
def get_memos():
	"""
	Returns all memos in the database, in a form that
	can be inserted directly in the 'session' object.
	"""
	records = [ ]
	for record in collection.find( { "type": "dated_memo" } ):
		record['date'] = arrow.get(record['date']).isoformat()
		#del record['_id']
		records.append(record)
		records.sort(key = lambda record:record['date'],reverse=True)
	return records 


if __name__ == "__main__":
	app.debug=CONFIG.DEBUG
	app.logger.setLevel(logging.DEBUG)
	app.run(port=CONFIG.PORT,host="0.0.0.0")

	
