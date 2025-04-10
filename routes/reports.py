from flask import Blueprint, render_template

from flask_login import login_required

reports = Blueprint('reports', __name__, url_prefix='/reports')

@reports.route('/')
@login_required
def index():
    return render_template('reports/index.html', title='Reports')

@reports.route('/dashboard')
@login_required
def dashboard():
    return render_template('reports/dashboard.html', title='Dashboard')