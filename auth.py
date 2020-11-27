from flask import render_template, redirect, url_for, request,jsonify,flash,json
import jwt
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, current_user, logout_user, login_required, current_user
from models import *
from controller import db,app
from flask import current_app
import datetime

# app.config.from_pyfile('config.cfg')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'token' in request.headers:
            # token = request.headers['token']
            user_session = session['token']
        if not token:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))

        try: 
    
            current_user =db.session.query(Admin).filter_by(logged_user=user_session).first()
            print("the token is", current_user)
        except:
            return redirect(url_for('login'))

        return f(current_user, *args, **kwargs)

    return decorated


# Initialize login manager
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return Admin.query.get(int(id))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method== 'POST':

        auth = request.form.get('password')

        email = request.form.get('email')
        password = request.form.get('password')
        print(password)
        remember = True if request.form.get('remember') else False

        user = Admin.query.filter_by(email=email).first()
    
        if not user and not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('login'))

        if check_password_hash(user.password, auth):
            token = jwt.encode({'public_id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
            print({'token' : token.decode('UTF-8')})    

        login_user(user)

        return redirect(url_for('addNewQuestions')) 
    return render_template('login.html')       

@app.route('/signup')
def signup():
    return render_template('Registration.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('username')
    password = request.form.get('password')

    user = Admin.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists.')
        return redirect(url_for('signup'))

    new_user =  Admin(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

 
@app.route('/add_users', methods=['GET','POST'])
@login_required
def add_users():  
    if request.method== 'POST':
        username = request.form.get('username')

        email = request.form.get('email')
        old_user = db.session.query(Add_SubUsers).filter(Add_SubUsers.useremail==email).all()
        if not old_user: 
            add_user= Add_SubUsers(username=username, useremail=email)
            db.session.add(add_user)
            db.session.commit()
            flash('New User '+username+' added' )
        else:
            flash(username+" has already added" )    
    return render_template('Add_users.html')       

