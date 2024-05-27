from flask import Flask, Blueprint, render_template, request, redirect, send_from_directory, url_for

nav_bp = Blueprint('nav', __name__)


## Nav
@nav_bp.route('/nav/home')
def nav_home():
    return render_template('nav/home.html')
