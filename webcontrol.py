import flask
import os
import diskolight

app = flask.Flask(__name__)
disko = diskolight.Diskolight()

@app.route("/")
def home(action="Start"):
    if not flask.session.get('logged_in'):
        return flask.render_template('login.html')
    else:
        return flask.render_template('main.html', action=action)

@app.route("/login", methods=["POST"])
def login():
    if flask.request.form['password'] == open("pwd.txt").read().strip() and flask.request.form['username'] == 'leddj':
        flask.session["logged_in"] = True
    else:
        flask.flash("You cannot pass!")
    return home()

@app.route("/start", methods=["GET", "POST"])
def start():
    if not flask.session.get("logged_in"):
        return flask.render_template("login.html")
    else:
        if not disko.running:
            disko.start()
            return home("Stop")
        else:
            disko.stop()
            return home("Start")

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host="192.168.2.125", port=80)
