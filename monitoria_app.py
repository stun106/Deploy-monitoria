# from app import create_app,db
from flask import Flask,render_template,redirect,url_for,request,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_required,login_user,logout_user
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import UserMixin
from datetime import datetime


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="stun106",
    password="korn1993",
    hostname="stun106.mysql.pythonanywhere-services.com",
    databasename="stun106$Monitoria_db",)
# "mysql+pymysql://root:@localhost/monitoria_db"
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret"

db = SQLAlchemy(app)

login_manager = LoginManager(app)

@login_manager.user_loader
def current_user(user_id):
    return Login.query.get(user_id)

class Login(db.Model,UserMixin):
    __tablename__ = "logins"
    id = db.Column(db.Integer, primary_key= True)
    userName = db.Column(db.String(50), nullable = False, unique = True)
    nickName = db.Column(db.String(50), nullable = False, unique = True)
    passWord = db.Column(db.String(255), nullable = False)
    turMa = db.Column(db.String(50),nullable = False)
    moduLo = db.Column(db.String(50),nullable = False)
    profile = db.relationship('Alunos', backref='login', lazy=True)

    def __init__(self) -> None:
        return self.userName

class Alunos(db.Model):
    __tablename__ = "alunos"
    id = db.Column(db.Integer, primary_key= True)
    fdBack = db.Column(db.String(255))
    satisfacao = db.Column(db.String(3))
    nickinfo = db.Column(db.String(80))
    pbDate = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('logins.id'))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register/", methods=["POST","GET"])
def register():
    if request.method == "POST":
        User = Login()
        User.userName = request.form["userName"].title()
        User.nickName = request.form["nickName"]
        User.passWord = generate_password_hash(request.form["passWord"])
        User.turMa = request.form["turMa"]
        User.moduLo = request.form["moduLo"].title()

        if not request.form["userName"] or not request.form["nickName"]:
            flash("Verifique Seus Dados ou Preencha os Campos Vazios.")
            return redirect(url_for("register"))
        db.session.add(User)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login/", methods=["POST","GET"])
def login():
    if request.method == "POST":
        nickName = request.form["nickName"]
        passWord = request.form["passWord"]
        user = Login.query.filter_by(nickName=nickName).first()
        print(user)

        if not user:
            flash("Verifique Seus Dados ou Preencha os Campos Vazios.")
            return redirect(url_for("login"))
        
        if not check_password_hash(user.passWord, passWord):
            flash("Verifique Seus Dados ou Preencha os Campos Vazios.")
            return redirect(url_for("login"))
        
        login_user(user)
        return redirect(url_for("profile",id=user.id))
    return render_template("login.html")

@app.route("/profile/<int:id>")
@login_required
def profile(id):
    Query = Login.query.filter_by(id=id).first()
    return render_template("profile.html", Query=Query)
        
@app.route("/profile/<int:id>", methods=["POST"])
def feed(id):
    if request.method == "POST":
        User = Login()
        dados = Alunos()
        dados.fdBack = request.form["fdBack"]
        dados.satisfacao = request.form["opcao"]
        dados.nickinfo = User.query.get(id)
        dados.pbDate = datetime.today()
        db.session.add(dados)
        db.session.commit()
        flash("Feedback enviado com Sucesso!.")
    Query=Login.query.filter_by(id=id).first()
    return render_template("profile.html", Query=Query)

@app.route("/logout")  # type: ignore
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True) 

