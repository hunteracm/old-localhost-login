from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

# database name based off of date name
now = datetime.datetime.now()
f = "data/{}.db".format(now.strftime("%Y-%m-%d"))

# configure database path
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{}".format(f)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# database setup
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)


# add an user to db
def add_to_db(d):
    db.session.add(User(fname=d['fname'], lname=d['lname'], email=d['email']))
    db.session.commit()


# routes begin here
@app.route('/')
def root():
    return render_template('index.html')


@app.route('/signin', methods=['POST'])
def signin():
    add_to_db(request.form.to_dict())
    return redirect(url_for('root'))


if __name__ == "__main__":
    db.create_all()
    app.debug = True
    app.run()
