from flask import Blueprint, render_template

from flask_login import login_required

billing = Blueprint('billing', __name__, url_prefix='/billing')

@billing.route('/')
@login_required
def index():
    return render_template('billing/index.html', title='Billing')