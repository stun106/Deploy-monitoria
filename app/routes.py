from app.models import Login,Alunos
from datetime import datetime
from flask import render_template, redirect,request, url_for,flash
from flask_login import login_user, logout_user,login_required
from app import db
from werkzeug.security import check_password_hash,generate_password_hash

def init_app(app):
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

#init_app factory de rotas