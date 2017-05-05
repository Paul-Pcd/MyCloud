#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.login import login_required, current_user
from .forms import AddTemplateForm, ModifyTemplateForm
from ..models import Template, Image
from ..extension import db
from ..decorators import admin_required

template = Blueprint('template', __name__, url_prefix = '/template')

@template.route('/', methods = ['GET','POST'])
@login_required
def index():
    if request.method == 'GET':
        form = AddTemplateForm()
        template_list = Template.query.filter().all()
        return render_template('template/index.html', form = form, template_list = template_list)
    else:
        if current_user.is_admin():
            form = AddTemplateForm(request.form)
            if form.validate_on_submit():
                template = Template()
                form.populate_obj(template)
                template_list = str(db.session.query(Template.template_name).filter(Template.template_name == template.template_name).all())
                if template.template_name not in template_list:
                    image_list = str(db.session.query(Image.id).filter(Image.id == template.image_id).all())
                    image_id = '(' + str(template.image_id) + 'L,)'
                    if image_id in image_list:
                        db.session.add(template)
                        db.session.commit()
                        return redirect(url_for('template.index'))
                    else:
                        return render_template("template/error.html", msg = "Image id '"+ str(image_id) + "' does not exist.")
                else:
                    return render_template("template/error.html",msg = "Template name '"+ str(template.template_name) + "' already exist.")

@template.route('/delete/<int:template_id>', methods = ['GET'])
@login_required
@admin_required
def delete(template_id):
    template = Template.query.filter(Template.id == template_id).first()
    if template:
        db.session.delete(template)
        db.session.commit()
    return redirect(url_for('template.index'))


@template.route('/modify/<int:template_id>', methods = ['POST'])
@login_required
@admin_required
def modify(template_id):
    template = Template.query.filter(Template.id == template_id).first()
    if template:
        new_template = Template()
        form = ModifyTemplateForm(request.form)
        form.populate_obj(new_template)
        image_list = str(db.session.query(Image.id).filter(Image.id == new_template.image_id).all())
        image_id = '(' + str(new_template.image_id) + 'L,)'
        if image_id in image_list:
            new_template.id = template.id
            db.session.delete(template)
            db.session.add(new_template)
            db.session.commit()
        else:
            return render_template("template/error.html", msg = "Image id '"+ str(image_id) + "' does not exist.")
    return redirect(url_for('template.index'))
