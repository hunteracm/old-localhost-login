from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.secret_key = "keysmithsmakekeys"


# configure database path
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/sign_ins.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# database setup
class User(db.Model):
    "Table to hold each member's data."
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    empl = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, nullable=False)


class signins(db.Model):
    "ID should reference a member. Table per meeting date."
    now = datetime.datetime.now()
    __tablename__ = now.strftime("%Y-%m-%d")
    id = db.Column(db.Integer, primary_key=True)
    empl = db.Column(db.Integer, nullable=False)


# add an user to db
def add_to_db(data):
    # TODO:
    # Perhaps load users into an list at startup and then compare to list,
    # and as users are added, add to db + list.
    # Check list for user, and create ac?
    # Check list for query for empl id
    if len(data['empl']) == 8 and data['empl'].isdigit():
        db.session.add(User(fname=data['fname'],lname=data['lname'],empl=int(data['empl']),email=data['email']))
        db.session.add(signins(empl=int(data['empl'])))
    else:
        flash('Bad empl id.')
    db.session.commit()


# routes begin here
@app.route('/')
def root():
    "Endpoint to render signin page."
    return render_template('index.html')


@app.route('/signin', methods=['POST'])
def signin():
    "Endpoint to add user data to database."
    add_to_db(request.form.to_dict())
    return redirect(url_for('root'))


if __name__ == "__main__":
    db.create_all()
    app.debug = True
    app.run()
