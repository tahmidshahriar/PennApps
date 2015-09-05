from flask import render_template, flash, redirect, request
from app import app
from .forms import LoginForm, LunchForm
import pymongo, time


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
	form = LoginForm()
	if form.validate_on_submit():
		try:
			conn=pymongo.MongoClient()
			db = conn.pennapps
			userInfo = db.userInfo
			print userInfo
			data = {}
			data['username'] = request.form['username']
			data['password'] = request.form['password']
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
			data['time'] = time.strftime("%d/%m/%y")
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
			return render_template('newsFeed.html', title='NewsFeed', myList = myList, form = form)
		
		except pymongo.errors.ConnectionFailure, e:
			print "Could not connect to MongoDB: %s" % e
			return render_template('newsFeed.html', title='NewsFeed', myList = myList, form = form)





