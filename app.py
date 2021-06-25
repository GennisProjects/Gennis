#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, request, url_for, abort, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from flask_uploads import UploadSet, IMAGES, configure_uploads
from sqlalchemy import String, Boolean, Integer, Column, ForeignKey, ARRAY, or_,and_, DateTime, DATE
from sqlalchemy.exc import SQLAlchemyError
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.security import generate_password_hash, check_password_hash


DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '123')
DB_NAME = os.getenv('DB_NAME', 'gennis-campus')
database_path = 'postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_path
app.config['UPLOADED_IMAGES_DEST'] = 'uploads/images'
app.config['UPLOADED_PHOTOS_ALLOW'] = {'png', 'jpg'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MAX_CONTENT_LENGTH'] = 2 * 922 * 1200
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = os.urandom(24)
app.secret_key = os.urandom(24)
images = UploadSet('images', IMAGES)

configure_uploads(app, images)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


def get_current_user():
    user_result = None
    if 'user' in session:
        user = session['user']
        user = Student.query.filter_by(username=user).first()
        user_result = user

    return user_result


def get_current_teacher():
    teacher_result = None
    if 'teacher' in session:
        user = session['teacher']
        user = Teachers.query.filter_by(username=user).first()
        teacher_result = user

    return teacher_result


class PhotoForm(FlaskForm):
    image = FileField('photo', validators=[FileRequired()])


@app.route('/photo_user', methods=['POST'])
def photo_add():
    user = get_current_user()
    try:
        if not user.gazalkent_admin and not user.director and not user.xojakent_admin and not user:
            return redirect(url_for('new_home'))
    except AttributeError:
        return redirect(url_for('new_home'))
    form = PhotoForm(meta={'csrf': False})
    if form.validate_on_submit():
        filename = images.save(form.image.data)
        image_url = images.url(filename)
        Student.query.filter_by(id=user.id).update({'photo': image_url})
        db.session.commit()
        flash("Фото профиля успешно обновлено")
        return redirect(url_for('new_home'))


@app.route('/photo_teacher', methods=['GET', 'POST'])
def photo_teacher():
    teacher = get_current_teacher()
    try:
        if not teacher:
            return redirect(url_for('new_home'))
    except AttributeError:
        return redirect(url_for('new_home'))
    form = PhotoForm(meta={'csrf': False})
    if form.validate_on_submit():
        filename = images.save(form.image.data)
        image_url = images.url(filename)
        Teachers.query.filter_by(id=teacher.id).update({'photo': image_url})
        db.session.commit()
        flash("Фото профиля успешно обновлено")
        return redirect(url_for('new_home'))


@app.route('/change_password', methods=['POST'])
def change_password():
    user = get_current_user()
    teacher = get_current_teacher()
    try:
        if not user and not teacher:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        username_database = Student.query.filter_by(username=username).first()
        teacher_username = Teachers.query.filter_by(username=username).first()
        if username_database:
            if username_database.username != user.username:
                return "Это имя пользователя уже занято"
        if teacher_username:
            if teacher_username.username != teacher.username:
                return "Это имя пользователя уже занято"
        new_password = generate_password_hash(password,method='sha256')
        if user:
            Student.query.filter_by(id=user.id).update({'password': new_password, 'username': username})
            db.session.commit()

        elif teacher:
            Teachers.query.filter_by(id=teacher.id).update({'password': new_password, 'username': username})
            db.session.commit()
        flash('Данные успешно изменены')
        return redirect(url_for('new_home'))


@app.template_filter('time_since')
def time_since(delta):
    seconds = delta.total_seconds()
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    if days > 0:
        return '%dd' % days + 'ays'
    elif hours > 0:
        return '%dh' % hours + 'ours'
    elif minutes > 0:
        return '%dm' % minutes + 'inutes'
    else:
        return 'только сейчас'


from base_route import *
from admin import *
from admin2 import *
from admin3 import *
from admin4 import *
from admin5 import *
from director import *
from teacher import *
from student import *
from subjects_function import *

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
