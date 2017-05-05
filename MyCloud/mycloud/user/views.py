#!/usr/bin/env python
#-*- coding: utf-8 -*-
#视图模块，每个blueprint对应一个处理函数

from flask import abort, Blueprint, current_app, render_template, request, redirect, url_for
from flask.ext.login import login_required, current_user
from ..models import User
from .forms import AddUserForm
from functools import wraps
from ..decorators import admin_required
from ..extension import db


user = Blueprint('user', __name__, url_prefix = '/user')

@user.route('/', methods = ['GET'])
@login_required
def index():
    return render_template('user/index.html')

@user.route('/admin', methods = ['GET'])
@login_required
@admin_required
def admin():
    users = User.query.filter().all()
    form = AddUserForm()
    return render_template('user/admin.html', users = users, form = form)

@user.route('/add', methods = ['GET', 'POST'])
@login_required
@admin_required
def add():
    if request.method == 'GET':
        form = AddUserForm()
        user_list = User.query.filter().all()
        return render_template('user/admin.html', users = users)
    else:
        form = AddUserForm(request.form)
        if form.validate_on_submit():
            user = User()
            form.populate_obj(user)
            db.session.add(user)
            db.session.commit()
        return redirect(url_for('user.admin'))


@user.route('/delete/<int:user_id>', methods = ['GET'])
@login_required
@admin_required
def delete(user_id):
    user = User.query.filter(User.id == user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('user.admin'))
