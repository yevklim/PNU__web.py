from flask import request, render_template
from time import time, ctime
from os import uname

from . import portfolio_blueprint
from .data import skills_list, projects_list

system_info = f"{uname().sysname} {uname().release} {uname().machine}"

@portfolio_blueprint.route('/', methods=["GET"])
def main():
    return render_template("portfolio/main.html", system_info=system_info, user_agent=request.user_agent, now=ctime(time()))

@portfolio_blueprint.route('/projects', methods=["GET"])
def projects():
    return render_template("portfolio/projects.html", projects_list=projects_list)

@portfolio_blueprint.route('/skills/', methods=["GET"])
@portfolio_blueprint.route('/skills/<int:idx>', methods=["GET"])
def skills(idx=None):
    if idx is not None:
        return render_template("portfolio/skill.html", skills_list=skills_list, idx=idx)
    else:
        return render_template("portfolio/skills.html", skills_list=skills_list)

@portfolio_blueprint.route('/about', methods=["GET"])
def about():
    return render_template("portfolio/about.html")
