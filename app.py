from flask import Flask, session
from flask import render_template, url_for, request, redirect
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = b'_5kmjiuhygtcuvib2u3biyuv90876rtxfcgvbi'

mongoConnect = MongoClient()
client = MongoClient('localhost', 27017)
db = client.sisdb


# USER LOGIN
@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        return userLogin(request)
    else:
        return render_template('login.html')


def userLogin(request):
    loginEmail = request.form['userLoginEmail']
    loginPsd = request.form['userLoginPsd']

    # check user in database
    newUser = db.user.find_one({"email": loginEmail})

    if newUser == None:  # user doesn't exist
        return 'Sorry This Not Registered A User'
    elif newUser['password'] != loginPsd:  # user exist
        return 'Wrong password'
    else:
        session['user'] = loginEmail
        # return 'volla!'
        return redirect(url_for('user'))


@app.route('/user', methods=['POST', 'GET'])
def user():

    if request.method == 'POST':
        return newRecord(request)
    else:
        if 'user' in session:
            return render_template('user.html', user_email=session['user'])
        else:
            return redirect(url_for('login'))


def newRecord(request):
    user_firstname = request.form['firstname']
    user_lastname = request.form['lastname']
    user_regno = request.form['regno']
    user_domain = request.form['domain']
    user_year = request.form['year']
    user_bdate = request.form['bdate']
    user_address = request.form['address']

    existingRecord = db.user.find_one({"regno": user_regno})

    if existingRecord != None:
        return ' This Registration Number Already Exist'
    else:
        db.user.insert_one({
            "firstname": user_firstname,
            "lastname": user_lastname,
            "regno": user_regno,
            "domain": user_domain,
            "year": user_year,
            "bdate": user_bdate,
            "bdate": user_bdate,
            "address": user_address,
        })
        return render_template('user.html', user_email=session['user'], notification_text='User Added')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


# USER DELETE
@app.route('/user_del')
def user_del():
    return render_template('user_del.html')


# USER SEARCH
@app.route('/user_src')
def user_src():
    return render_template('user_src.html')


# USER UPDATE
@app.route('/user_update')
def user_update():
    return render_template('user_update.html')


# SUPER USER
@app.route('/sudo')
def sudo():
    return render_template('sudo.html')


# VIEW ALL USER
@app.route('/all_user', methods=['GET'])
def view_all():
    return ShowallUser()


def ShowallUser():
    userList = []
    allUser = db.user.find()
    for user in allUser:
        userList.append(user)
    return render_template('all_user.html', userList=userList)


# REMOVE USER
@app.route('/removeuser', methods=['POST', 'GET'])
def removeUser():
    if request.method == 'GET':
        return 'hello'
    else:
        return redirect(url_for('/all_user'))


# ADD A USER
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        return CreateUser(request)
    else:
        print('something went wrong')
        return render_template('add_user.html')


def CreateUser(request):
    userEmail = request.form['email']
    userPassword = request.form['password']

    UserExist = db.user.find_one({"email": userEmail})

    if UserExist != None:
        print('UserExist')
        return " this user already exist"
    else:
        print('NOT UserExist')
        db.user.insert_one({"email": userEmail, "password": userPassword})
        return redirect(url_for('sudo'))


# DEBUGGER
app.run(debug=True)
