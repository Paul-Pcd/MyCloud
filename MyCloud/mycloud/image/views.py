#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.login import login_required, current_user
from werkzeug import secure_filename
from .forms import AddImageForm
from ..models import Image
from ..extension import db
from ..decorators import admin_required
import os

image = Blueprint('image', __name__, url_prefix = '/image')

@image.route('/', methods = ['GET','POST'])
@login_required
def index():
    if request.method == 'GET':
        form = AddImageForm()
        image_list = Image.query.filter().all()
        return render_template('image/index.html', form = form, image_list = image_list)
    else:
        if current_user.is_admin(): 
            form = AddImageForm(request.form)
            if form.validate_on_submit():
                image = Image()
                form.populate_obj(image)
                image_name, image_path, image_list = str(image.image_name), str(image.image_path), str(Image().query.filter().all())
                res = os.popen('find %s -name %s -maxdepth 1 | wc -l'%(image_path,image_name)).read().strip()
                if res == '0':
                    msg = 'Image name "%s" is not exists in "%s".' %(image_name, image_path)
                    return render_template('image/error.html', msg = msg)
                if image_name in image_list :
                    msg = 'Image "%s" already exists.' %(image_name)
                    return render_template('image/error.html', msg = msg)

                db.session.add(image)
                db.session.commit()
            return redirect(url_for('image.index'))
        else:
            return render_template('image/index.html', form = form, image_list = image_list)
@image.route('/delete/<int:image_id>', methods = ['GET'])
@login_required
@admin_required
def delete(image_id):
    image = Image.query.filter(Image.id == image_id).first()
    if image:
        db.session.delete(image)
        db.session.commit()
    return redirect(url_for('image.index'))

@image.route('/discover')
@login_required
@admin_required
def discover():
    image_path = '/root/workspace/MyCloud/images/'
    image_add_list = os.popen('ls %s'%(image_path)).read().strip().split('\n')
    images = [ str(i.image_name) for i in Image.query.filter().all()]    # 取出数据库中存在的镜像名并转化为字符串格式，存入列表
    for image_name in image_add_list:
        image_name = unicode(image_name)
        if image_name not in images:    #如果查找本地目录发现的新镜像不在数据库中
            image = Image()
            image.image_name = image_name
            image.image_path = '/root/workspace/MyCloud/images/'
            image.status_code = 1
            db.session.add(image)
    db.session.commit()
    return redirect(url_for('image.index'))
