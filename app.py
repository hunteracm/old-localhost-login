from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.secret_key = "keysmithsmakekeys"


# configure database path
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/sign_ins.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(app)

# variables for app
TODAY = datetime.datetime.now().strftime("%Y-%m-%d")
today_id = None
users = None


# database setup
class User(DB.Model):
    "Table to hold each member's data."
    id = DB.Column(DB.Integer, primary_key=True)
    fname = DB.Column(DB.String, nullable=False)
    lname = DB.Column(DB.String, nullable=False)
    empl = DB.Column(DB.Integer, nullable=False)
    email = DB.Column(DB.String, nullable=False)


class Meetings(DB.Model):
    "ID should reference a member. Table per meeting date."
    id = DB.Column(DB.Integer, primary_key=True)
    date = DB.Column(DB.String, nullable=False)


class Signins(DB.Model):
    "ID should reference a member. Table per meeting date."
    id = DB.Column(DB.Integer, primary_key=True)
    user_id = DB.Column(DB.Integer, nullable=False)
    meeting_id = DB.Column(DB.Integer, nullable=False)


# add an user to DB
def add_to_db(data):
    "Add log in"
    c_u = User(fname=data['fname'], lname=data['lname'], empl=int(data['empl']), email=data['email'])
    if not (len(data['empl']) == 8 and data['empl'].isdigit()):
        flash('Bad empl id.')
    else:
        if not User.query.filter_by(empl=c_u.empl).first():
            DB.session.add(c_u)
            DB.session.commit()
        c_id = User.query.filter_by(empl=c_u.empl).first().id
        DB.session.add(Signins(user_id=c_id, meeting_id=today_id))
        DB.session.commit()
    DB.session.commit()


# routes begin here
@app.route('/')
def root():
    "Endpoint to render signin page+sets up meetings DB/ fetches information."
    if not Meetings.query.filter_by(date=TODAY).first():
        DB.session.add(Meetings(date=TODAY))
        DB.session.commit()
    global today_id
    today_id = Meetings.query.filter_by(date=TODAY).first().id
    global users
    users = User.query.order_by(User.id).all()
    return render_template('index.html', u=users)


@app.route('/signin', methods=['POST'])
def signin():
    "Endpoint to add user data to database."
    add_to_db(request.form.to_dict())
    return redirect(url_for('root'))


if __name__ == "__main__":
    DB.create_all()
    app.debug = True
    app.run()
