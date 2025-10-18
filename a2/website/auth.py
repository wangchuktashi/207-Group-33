# website/auth.py
from flask import Blueprint, flash, render_template, request, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        first_name     = form.first_name.data.strip()
        surname        = form.surname.data.strip()
        email          = form.email_id.data.strip()
        password       = form.password.data
        mobile_number  = form.mobile_number.data.strip()
        street_address = form.street_address.data.strip()

        # Uniqueness checks (email, mobile are unique in your model)
        if db.session.scalar(db.select(User).where(User.email_id == email)):
            flash('An account with this email already exists.', 'warning')
            return redirect(url_for('auth.register'))

        if db.session.scalar(db.select(User).where(User.mobile_number == mobile_number)):
            flash('That mobile number is already in use.', 'warning')
            return redirect(url_for('auth.register'))

        user = User(
            first_name=first_name,
            surname=surname,
            email_id=email,
            password_hash=generate_password_hash(password),
            mobile_number=mobile_number,
            street_address=street_address
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('user.html', form=form, heading='Register')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email_id.data.strip()
        pwd   = form.password.data

        user = db.session.scalar(db.select(User).where(User.email_id == email))
        if not user:
            flash('No account found for that email.', 'danger')
        elif not check_password_hash(user.password_hash, pwd):
            flash('Incorrect password.', 'danger')
        else:
            login_user(user)
            nextp = request.args.get('next')
            if not nextp or not nextp.startswith('/'):
                nextp = url_for('main.index')
            return redirect(nextp)

    return render_template('user.html', form=form, heading='Login')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('main.index'))