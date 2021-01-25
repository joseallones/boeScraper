
from flask import Flask, render_template
import os
from storage import Storage

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
from flask import request
import datetime


@app.route("/")
def home():
    rama = request.args.get('rama')
    post_jobs = Storage.load_last_file()
    date = Storage.get_date(Storage.last_file())
    return render_template("home.html", post_jobs=post_jobs, date=date, rama=rama)


@app.route("/history")
def history():
    rama = request.args.get('rama')
    post_jobs = Storage.load_history_file()
    date = datetime.datetime.strptime("2020-09-02", '%Y-%m-%d')
    return render_template("home.html", post_jobs=post_jobs, date=date, rama=rama, check_is_active='false')


if __name__ == '__main__':
    app.run()