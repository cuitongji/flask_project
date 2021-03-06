# coding: utf-8
import shelve
from datetime import datetime

from flask import Flask, request, render_template, redirect,escape,Markup

application = Flask(__name__)

DATA_FILE = 'guestbook.dat'

def save_data(name,comment,create_at):
	"""Save the comment data"""
	# open the shelve module database File
	database = shelve.open(DATA_FILE)
	# if there is no greeting_list in database, create it.
	if 'greeting_list' not in database:
		greeting_list=[]
	else:
		# get the greeting_list form database
		greeting_list = database['greeting_list']
	# append the data into the list top
	greeting_list.insert(0,{
	                     'name':name,
	                     'comment':comment,
	                     'create_at':create_at,
	                     })
	# update the database
	database['greeting_list'] = greeting_list

	# close the database file
	database.close()

def load_data():
	"""Return the comment data saved before"""
	# open the shelve module database file
	database = shelve.open(DATA_FILE)

	# get the greeting_list. if not, just return empty list.
	greeting_list = database.get('greeting_list',[])

	database.close()
	return greeting_list

@application.route('/')
def index():
	"""Top page
	Use template to show the page
	"""

	# read the comment data
	greeting_list=load_data()
	return render_template('index.html',greeting_list=greeting_list)

@application.route('/post',methods=['POST'])
def post():
	"""
	Comment's target url
	"""
	# get the comment data
	name = request.form.get('name')
	comment = request.form.get('comments')
	create_at = datetime.now()
	# save_data
	save_data(name,comment,create_at)
	# redirect to the top page
	return redirect('/')

if __name__ == '__main__':
	# Run the application when the IP address is 127.0.0.1 and the port is 5000
	application.run('127.0.0.1',5000,debug=True)