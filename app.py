from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/signin', methods=['POST'])
def signin():
    result = request.form
    # add to database after mini parsing
    return redirect(url_for('root'))


if __name__ == "__main__":
    app.debug = True
    app.run()
