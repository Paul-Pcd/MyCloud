#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.login import login_required
from .forms import AddHostForm
from ..models import Host, VM
from ..extension import db
from ..decorators import admin_required

host = Blueprint('host', __name__, url_prefix = '/hosts')

@host.route('/', methods = ['GET','POST'])
@login_required
@admin_required
def index():
    if request.method == 'GET':
        form = AddHostForm()
        host_list = Host.query.filter().all()
        return render_template('host/index.html', form = form, host_list = host_list)
    else:
        form = AddHostForm(request.form)
        if form.validate_on_submit():
            host = Host()
            form.populate_obj(host)
            host_list = str(db.session.query(Host.ip).all())
            host_ip = '(u\''+str(host.ip)+'\',)'
            if host_ip not in host_list:
                vm_list = VM.query.filter(VM.host_ip == host.ip).all()
                host.vm_list = '; '.join([ str(i.vm_name) for i in vm_list ])
                db.session.add(host)
                db.session.commit()
            else:
                 return render_template("host/error.html",msg = "Host ip '"+ str(host.ip) + "' already exist.")
        return redirect(url_for('host.index'))

@host.route('/delete/<int:host_id>', methods = ['GET'])
@login_required
@admin_required
def delete(host_id):
    host = Host.query.filter(Host.id == host_id).first()
    if host:
        host_vms = VM.query.filter(VM.host_ip == host.ip).all()
        for vm in host_vms:
            db.session.delete(vm)
        db.session.delete(host)
        db.session.commit()
        
    return redirect(url_for('host.index'))

