#!./.env/bin/python

from os import uname
import time
from flask import Flask, request, render_template, redirect, url_for
from data import skills_list, projects_list
system_info=f"{uname().sysname} {uname().release} {uname().machine}"

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html", system_info=system_info, user_agent=request.user_agent, now=time.ctime(time.time()))

@app.route('/projects')
def projects():
    return render_template("projects.html", projects_list=projects_list)

@app.route('/skills/')
@app.route('/skills/<int:idx>')
def skills(idx=None):
    if idx is not None:
        return render_template("skill.html", skills_list=skills_list, idx=idx)
    else:
        return render_template("skills.html", skills_list=skills_list)

@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(debug=True)