from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import LoginForm
from ..models import User
from .. import db


@auth.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():

        set_db_seed()

        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)

            return redirect(url_for('home.dashboard'))

        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))


def set_db_seed():

    exists = db.session.query(User).filter_by(email='admin@admin.com').first()

    if not exists:
        user = User(
            email='admin@admin.com',
            first_name='admin',
            last_name='admin',
            password='admin',
            is_admin=True
        )

        print(user)
        db.session.add(user)
        db.session.commit()