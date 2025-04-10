from flask import Blueprint, render_template

from flask_login import login_required

laboratory = Blueprint('laboratory', __name__, url_prefix='/laboratory')

@laboratory.route('/')
@login_required
def index():
    return render_template('laboratory/index.html', title='Laboratory')