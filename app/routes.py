from app import app, db
from flask import url_for, redirect, render_template, flash, request
from flask_login import current_user, login_user, logout_user, current_user, login_required
import sqlalchemy as sa
from app.models import User
from app.forms import LoginForm, RegistrationForm
from urllib.parse import urlsplit

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Homepage')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid login or password.')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations! You are now registered.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', form=form)

@app.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = CreationForm()
    if form.validate_on_submit():
        event = Event(title=form.title.data,
                      description=form.description.data,
                      date=form.date.data,
                      location=form.location.data,
                      total_seats=form.total_seats.data,
                      seats_left=form.total_seats.data,
                      created_by=current_user.username)
        db.session.add(event)
        db.session.commit()
        flash('Congratulations, your event was successfully added!')
        return redirect(url_for('dashboard'))
    return render_template('create_event.html', title='Create an event', form=form)