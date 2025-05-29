from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from models import User, db
from forms import LoginForm, RegistrationForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            is_employer=form.is_employer.data
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title='Register', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page or url_for('home'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')

    return render_template('auth/login.html', title='Login', form=form)

@auth_bp.route('/logout')
def logout():
    """Handle user logout."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))
