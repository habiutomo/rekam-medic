from flask import Blueprint, render_template

from flask_login import login_required

documents = Blueprint('documents', __name__, url_prefix='/documents')

@documents.route('/')
@login_required
def index():
    return render_template('documents/index.html', title='Documents')