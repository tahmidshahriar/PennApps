from flask import render_template, flash, redirect, request, session
from app import app
from .forms import LoginForm, LunchForm, SignupForm
import pymongo, time
from twilio.rest import TwilioRestClient

@app.route('/')
@app.route('/index')
def index():
    user1= {'nickname': 'Arvind',
    		'statement': 'Fuck you Tahmid'} 
    user2= {'nickname': 'Tahmid',
    		'statement': 'But Whyyyyyyyyy'} # fake user
    return render_template('index.html',
                           title='Home',
                           user1=user1,
                           user2=user2)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()
	if form.validate_on_submit():
		try:
			conn=pymongo.MongoClient()
			db = conn.pennapps
			userInfo = db.userInfo
			print userInfo
			data = {}
			data['username'] = request.form['username']
			data['password'] = request.form['password']
			data['firstname'] = request.form['firstname']
			data['lastname'] = request.form['lastname']
			data['phone'] = request.form['phone']
			data['email'] = request.form['email']
			userInfo.insert(data)
			return redirect('/index')

		except pymongo.errors.ConnectionFailure, e:
			print "Could not connect to MongoDB: %s" % e
			return redirect('/index')
	else:
		return render_template('signup.html', title='Sign Up', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		try:
			conn=pymongo.MongoClient()
			db = conn.pennapps
			userInfo = db.userInfo
			usernameToVerify = list(userInfo.find({'username': request.form['username']}))
			if(len(usernameToVerify) == 0):
				return redirect('/login')
			elif(request.form['password'] == usernameToVerify[0]['password']):
				session['loggedinName'] = usernameToVerify[0]['firstname'] + usernameToVerify[0]['lastname']
				session['loggedinPhone'] = usernameToVerify[0]['phone']
				return redirect('/newsFeedStuff')
			else:
				return redirect('/login')

		except pymongo.errors.ConnectionFailure, e:
			print "Could not connect to MongoDB: %s" % e
			return redirect('/index')
	else:
		return render_template('login.html', title='Sign In', form=form)


@app.route('/newsFeedStuff', methods=['GET', 'POST'])
def newsFeedStuff():
	form = LunchForm()
	if form.validate_on_submit():
		try:
			conn=pymongo.MongoClient()
			db = conn.pennapps
			lunchDetails = db.lunchDetails
			data = {}
			data['title'] = request.form['title']
			data['post'] = request.form['post']
			data['time'] = time.strftime("%m/%d/%y")
			data['name'] = session['loggedinName']
			data['phone'] = session['loggedinPhone']
			
			lunchDetails.insert(data)
			return redirect('/newsFeedStuff')

		except pymongo.errors.ConnectionFailure, e:
			print "Could not connect to MongoDB: %s" % e
			return redirect('/newsFeedStuff')
	else:
		try:
			conn=pymongo.MongoClient()
			db = conn.pennapps
			lunchDetails = db.lunchDetails
			myList = list(lunchDetails.find())
			return render_template('newsFeed.html', title='NewsFeed', myList = myList, form = form, myFunc = twilioMessage)
		
		except pymongo.errors.ConnectionFailure, e:
			print "Could not connect to MongoDB: %s" % e
			return render_template('newsFeed.html', title='NewsFeed', myList = myList, form = form, myFunc = twilioMessage)

@app.route('/sendMessage/<number>', methods=['GET', 'POST'])
def twilioMessage(number):
	# Your Account Sid and Auth Token from twilio.com/user/account
	account_sid = "ACe35ea76b49265923ca76b9e678ce2893"
	auth_token  = "369e13949b072a54ab72b3e8547f226d"
	client = TwilioRestClient(account_sid, auth_token)
	 
	message = client.messages.create(body=session['loggedinName'] + " would like to contact you for lunch. If interested, please responded at " + session['loggedinPhone'],
	    to=number,    # Replace with your phone number
	    from_="+16463625482") # Replace with your Twilio number
	return redirect('/newsFeedStuff')

