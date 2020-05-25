import os
import sys
from flask import render_template, url_for, flash, redirect, request, Blueprint, session
from flask_login import login_user, current_user, logout_user, login_required
from app.models import User
from app.users.forms import LoginForm, AddUserForm
from app.users.utils import search_user, create_user, change_user_permission, delete_user_from_grafana

users = Blueprint('users', __name__)

GRAFANA_HOST = os.environ.get('GRAFANA_HOST')
if not GRAFANA_HOST:
    raise ValueError("Please set environment variable GRAFANA_HOST")


# https://grafana.com/docs/grafana/latest/http_api/user/#search-users
# https://grafana.com/docs/grafana/latest/http_api/admin/#delete-global-user
# https://grafana.com/docs/grafana/latest/http_api/admin/#permissions
# https://grafana.com/docs/grafana/latest/http_api/admin/#global-users

SEARCH_API_URL = f'{GRAFANA_HOST}/api/users'
USERS_API_URL = f'{GRAFANA_HOST}/api/admin/users'


@users.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.add_user'))
    form = LoginForm()
    if form.validate_on_submit():
        status_code, users_list = search_user(url=SEARCH_API_URL, username=form.username.data, password=form.password.data)
        if status_code == 401:
            flash('Invalid username or password', 'danger')
        elif status_code == 403:
            flash('You must be an admin user for adding users', 'danger')
        else:
            session['username'] = form.username.data
            session['password'] = form.password.data
            for user in users_list:
                if user.get('login') == form.username.data:
                    loginuser_json = user
                    if loginuser_json:
                        loginuser = User(loginuser_json)
                        login_user(loginuser, remember=form.remember.data)
                        next_page = request.args.get('next')
                        return redirect(next_page) if next_page else redirect(url_for('users.login'))
                    else:
                        flash('Invalid email or password', 'danger')

    return render_template('login.html', title='Login', form=form)


@users.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        payload = {
            'name': form.name.data,
            'email': form.email.data,
            'login': form.username.data,
            'password': form.password.data,
            'OrgId': 1
        }
        username = session['username']
        password = session['password']
        status_code, data = create_user(url=USERS_API_URL, username=username, password=password, payload=payload)
        if status_code == 500:
            flash('User already exists', 'warning')
        elif form.is_admin.data:
            user_id = data["id"]
            payload = {
                'isGrafanaAdmin': True
            }
            url = f'{USERS_API_URL}/{user_id}/permissions'
            status_code, data = change_user_permission(url=url, username=username, password=password, payload=payload)
            if status_code != 200:
                url = f'{USERS_API_URL}/{user_id}'
                status_code, data = delete_user_from_grafana(url=url, username=username, password=password)
                flash('Something went wrong!', 'danger')
            else:
                flash('User has been created successfully', 'success')
        else:
            flash('User has been created successfully', 'success')

        return redirect(url_for('users.login'))
    return render_template('add_user.html', title='Add User', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))

