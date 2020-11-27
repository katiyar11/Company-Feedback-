from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager 
from flask_mail import Mail
from elasticsearch import Elasticsearch

mail = Mail()

db = SQLAlchemy()

app = Flask(__name__)
es = Elasticsearch([{'host': 'localhost', 'port': 5000}])   
   

app.config['SECRET_KEY'] = 'thisismysecretkeyhjkui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:root@localhost:8080/Feedback_DB'   
app.config['URL'] = "http://127.0.0.1:5000/"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True

db.init_app(app)

# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'
# login_manager.init_app(app)

# from models import Admin

# @login_manager.user_loader
# def load_user(user_id):
#     return Admin.query.get(int(user_id))