from flask  import Flask, Response, jsonify,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

#init flask app with the database and everything
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["SECRET_KEY"]="supersecretkey"

#init the database
db=SQLAlchemy(app)
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"


#now we create user class to store about the user by inheriting from UserMixin and db.Model that will create blue_print of the user
class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(250),unique=True,nullable=False)
    password=db.Coulmn(db.String(250),nullable=False)


#this creates the dbase
with app.app_context():
    db.create_all()

@login_manager.userloader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return render_template("index.html")


#checkin in

if __name__=="__main__":
    app.run(debug=True)