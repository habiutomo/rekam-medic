from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from models import User, Role
from forms import LoginForm, RegistrationForm

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page if next_page else url_for('index'))
        else:
            flash('Login failed. Please check your username and password.', 'danger')
    
    return render_template('auth/login.html', title='Login', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

@auth.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if not current_user.role.name == 'admin':
        flash('Only administrators can register new users.', 'warning')
        return redirect(url_for('index'))
        
    form = RegistrationForm()
    form.role.choices = [(role.id, role.name) for role in Role.query.all()]
    
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            role_id=form.role.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'User {form.username.data} created successfully!', 'success')
        return redirect(url_for('auth.users'))
        
    return render_template('auth/register.html', title='Register New User', form=form)

@auth.route('/users')
@login_required
def users():
    if not current_user.role.name == 'admin':
        flash('Only administrators can access user management.', 'warning')
        return redirect(url_for('index'))
        
    users = User.query.all()
    return render_template('auth/users.html', title='User Management', users=users)

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('auth/profile.html', title='My Profile')

@auth.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.role.name == 'admin':
        flash('Only administrators can delete users.', 'danger')
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('auth.users'))
        
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {user.username} has been deleted.', 'success')
    return redirect(url_for('auth.users'))