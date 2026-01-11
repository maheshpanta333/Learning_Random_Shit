from flask  import Flask, Response, jsonify,render_template,url_for,redirect,request
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
    password=db.Column(db.String(250),nullable=False)


#this creates the dbase
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return render_template("index.html")


#now for the user sign up and for form we need post as well
@app.route("/register",methods=["GET","POST"])
def register_user():
    if request.method =="POST":
        username=request.form.get("username")
        password=request.form.get("password")
#here we see if there is such username and .first returns the first row
        if User.query.filter_by(username=username).first():
            return render_template("index.html",error="Username  taken!")
        
        hashed_password=generate_password_hash(password=password,method="pbkdf2:sha256")
        password=""
        new_user=User(username=username,password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return render_template("success_page.html")


if __name__=="__main__":
    app.run(debug=True)