import os
import time

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from wtforms import Form, StringField, TextAreaField, validators

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]
auth = HTTPBasicAuth()

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    bio = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<User {self.name}>"


class NewUserForm(Form):
    name = StringField("Name", [validators.Length(min=1, max=80)])
    bio = TextAreaField("Bio")


@auth.verify_password
def verify_password(username, password):
    return username == "admin" and password == "password"


@app.route("/")
def show_all():
    users = User.query.all()
    return render_template("index.html.tmpl", users=users)


@app.route("/admin/new", methods=["GET", "POST"])
@auth.login_required
def admin():
    form = NewUserForm(request.form)
    if request.method == "POST" and form.validate():
        user = User(name=form.name.data, bio=form.bio.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("show_all"))

    return render_template("admin.html.tmpl", form=form)


if __name__ == "__main__":
    time.sleep(5)
    with app.app_context():
        db.create_all()
