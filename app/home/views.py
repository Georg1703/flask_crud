from flask import flash, redirect, render_template, url_for, request, send_file, current_app
from flask_login import login_required, login_user, logout_user
import requests
import aiohttp
import asyncio
import json
import time
import os

from . import home
from .. import db
from ..models import User


@home.route('/')
def homepage():
    """Manage the / route"""
    return render_template('home/index.html', title="Welcome")


@home.route('/dashboard')
@login_required
def dashboard():
    """Manage the /dashboard route"""
    users_list = db.session.query(User).all()
    return render_template('home/dashboard.html', title="Dashboard", users_list=users_list)


@home.route('/add_user', methods=['POST'])
def add_user():

    is_admin = False
    if len(request.form['rights']) > 0 and request.form['rights'] == '1':
        is_admin = True

    user = User(
        email=request.form['email'],
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        password=request.form['password'],
        is_admin=is_admin
    )

    # add user to the database
    db.session.add(user)
    db.session.commit()

    flash('You have successfully added user.')
    return redirect(url_for('home.dashboard'))


@home.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete_user(id):
    user = db.session.query(User).filter(User.id == id)
    user.delete()
    db.session.commit()

    flash('User removed successfully')

    return redirect(url_for('home.dashboard'))


@home.route('/edit/<int:id>', methods=['GET'])
@login_required
def get_user(id):

    user = db.session.query(User).where(User.id == id).first()

    return render_template('/home/edit.html', user=user, title='Edit user')


@home.route('/update/<int:id>/', methods=['POST'])
@login_required
def update_user(id):

    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    is_admin = bool(int(request.form['rights']))

    db.engine.execute(f"UPDATE users SET "
                      f"email = '{email}', "
                      f"first_name = '{first_name}', "
                      f"last_name = '{last_name}',"
                      f"is_admin = {is_admin} WHERE id = {id}")

    flash('You have successfully updated user.')
    return redirect(url_for('home.dashboard'))


async def get(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.read()
                return json.loads(data)
    except:
        pass


@home.route('/asynchronous')
def asynchronous():
    start_time = time.time()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    url_list = ['http://localhost:5000/json/file_1.json',
                'http://localhost:5000/json/file_2.json',
                'http://localhost:5000/json/file_3.json']

    coroutines = [get(url) for url in url_list]

    result = loop.run_until_complete(asyncio.gather(*coroutines))
    sorted_result = sort_received_result(result)

    spend_time = f'--- {time.time() - start_time} seconds ---'

    return render_template('/home/json_result.html', result=sorted_result, spend_time=spend_time)


@home.route('/synchronous')
def synchronous():
    start_time = time.time()

    url_list = ['http://localhost:5000/json/file_1.json',
                'http://localhost:5000/json/file_2.json',
                'http://localhost:5000/json/file_3.json']

    result = [requests.get(url).json() for url in url_list]
    sorted_result = sort_received_result(result)

    spend_time = f'--- {time.time() - start_time} seconds ---'

    return render_template('/home/json_result.html', result=sorted_result, spend_time=spend_time)


@home.route('/json/<path:path>')
def get_json_file(path):
    with current_app.open_resource(f'static/json/{path}') as f:
        return f.read()


def sort_received_result(result: list) -> list:

    result_list = []
    for list in result:
        result_list += list

    return sorted(result_list, key=lambda i: i['id'])
