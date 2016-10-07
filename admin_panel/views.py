import os

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user

from admin_panel import app, db, login_manager
from forms import LoginForm, ScanForm, CreateUserForm
from models import User, Scan

from scanners import pathmaker
from scanners.vetbiz import vetbiz_scraper, vetbiz_converter


# Pages

# index (home page)
@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', recent_scans=Scan.recent(10))


# scan page
@app.route('/scan', methods=['GET', 'POST'])
@login_required
def scan():
    # TODO: turn this into a loop, a class, or something other than hard-coded repetition (post-prototype).
    form = ScanForm()
    # vetbiz
    last_datetime = 0
    last_count = 0
    last_diff = 0
    last_user = 'N/A'
    if Scan.last_scan('vetbiz').count() > 0:
        last_scan = Scan.last_scan('vetbiz')[0]
        last_datetime = last_scan.datetime
        last_count = last_scan.count
        last_diff = last_scan.diff
        last_user = last_scan.user.username
    form.vetbiz_last_scan = last_datetime
    form.vetbiz_data_count = last_count
    form.vetbiz_new_data = last_diff
    form.vetbiz_invoked_by = last_user
    # buyvet
    last_datetime = 0
    last_count = 0
    last_diff = 0
    last_user = 'N/A'
    if Scan.last_scan('buyvet').count() > 0:
        last_scan = Scan.last_scan('buyvet')[0]
        last_datetime = last_scan.datetime
        last_count = last_scan.count
        last_diff = last_scan.diff
        last_user = last_scan.user.username
    form.buyvet_last_scan = last_datetime
    form.buyvet_data_count = last_count
    form.buyvet_new_data = last_diff
    form.buyvet_invoked_by = last_user
    # more scanners
    # ...
    if form.vetbiz_scan.data:
        last_count = form.vetbiz_data_count
        form.vetbiz_data_count = scan_vetbiz()  # grab from newly scanned data
        form.vetbiz_new_data = form.vetbiz_data_count - last_count
        scan = Scan(user=current_user,
                    name=form.vetbiz_title,
                    url=form.vetbiz_url,
                    count=form.vetbiz_data_count,
                    diff=form.vetbiz_new_data)
        db.session.add(scan)
        db.session.commit()
        flash("{} scan has been logged.".format(form.vetbiz_title))
    if form.buyvet_scan.data:
        last_count = form.buyvet_data_count
        form.buyvet_data_count = 0  # grab from newly scanned data
        form.buyvet_new_data = form.buyvet_data_count - last_count
        scan = Scan(user=current_user,
                    name=form.buyvet_title,
                    url=form.buyvet_url,
                    count=form.buyvet_data_count,
                    diff=form.buyvet_new_data)
        db.session.add(scan)
        db.session.commit()
        flash("{} scanner has not yet been produced.".format(form.buyvet_title))
    return render_template('scan.html', form=form)


# create user page
def create_user():
    form = CreateUserForm()
    return render_template('createuser.html', form=form)


# Scans

def scan_vetbiz():
    saved_directory = os.getcwd()
    vetbiz_scraper.run()
    # TODO: grab the total number of data items from the vetbiz site and divide by 100 for integer in arg.
    pathmaker.change_path(saved_directory)
    vetbiz_converter.run(91)
    pathmaker.change_path('scanners/csv_files')
    csv_file = open('vetbiz_data.csv')
    count = sum(1 for _ in csv_file) - 2  # minus first row (column names); minus 2nd to last row (hot-fix)
    # put it back where you found it from
    pathmaker.change_path(saved_directory)
    return count


# User

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


# Authentication

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember.data)
            flash('Logged in successfully as {}'.format(user.username))
            return redirect(request.args.get('next') or url_for('index', username=user.username))
        flash('Incorrect username or password.')
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


# Errors

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
