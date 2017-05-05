#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask.ext.login import login_required, current_user
from .forms import AddVMForm
from ..models import VM, Template, Image, Host
from ..extension import db
from ..decorators import admin_required
from ..virtscripts import VM_Assistant 
from datetime import datetime
import os
import paramiko

vm = Blueprint('vm', __name__, url_prefix = '/vm')

def remote_control(ip, port, username, password, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username, password)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    res = stdout.read()
    ssh.close()
    return res

def get_vm_list(host):
    cmd = cmd = 'virsh list --all | awk \'{if(NR>2) print $2}\''
    res = remote_control(host.ip, host.port, host.username, host.password, cmd)
    res = [ i for i in res.strip().split('\n') if i != '']
    return res    # 去除字符串中的空格、以换行符划分元素返回列表

def get_vm_status(vm_name, host):
    cmd = 'virsh list --all | grep \'%s\' | awk \'{print $3, $4}\''%(vm_name)
    res = remote_control(host.ip, host.port, host.username, host.password, cmd)
    return res

def get_host_existence(ip):
    ip_list = str(db.session.query(Host.ip).filter(Host.ip == ip).all())
    if ip in ip_list:
        host_status = str(db.session.query(Host.status_code).filter(Host.ip == ip).first()[0])
        if host_status == '1':
            return True
    return False

def open(vm, host):
    vnc_port = vm.vnc_port
    close(host)
    #cmd = 'nohup /root/workspace/MyCloud/mycloud/virtscripts/noVNC/utils/launch.sh --vnc localhost:%s &'%(vnc_port)
    #remote_control(host.ip, host.port, host.username, host.password, cmd)
    os.system('nohup /root/workspace/MyCloud/mycloud/virtscripts/noVNC/utils/launch.sh --vnc localhost:%s &'%(vnc_port))


def close(host):
    os.system('ps -aux | grep /utils/launch.sh | cut -c 9-15 | xargs kill')
    #cmd = 'ps -aux | grep /utils/launch.sh | cut -c 9-15 | xargs kill'
    #remote_control(host.ip, host.port, host.username, host.password, cmd)

# 创建虚拟机，根据模板
@vm.route('/', methods = ['GET','POST'])
@login_required
def index():
    if request.method == 'GET':    # 通过GET方法访问时直接返回虚拟机主页
        form = AddVMForm()
        vm_list = VM.query.filter().all()
        return render_template('vm/index.html', form = form, vm_list = vm_list)
    else:
        form = AddVMForm(request.form)
        if form.validate_on_submit():
            vm = VM()
            form.populate_obj(vm)
            if not get_host_existence(vm.host_ip):
                return render_template("vm/error.html",msg = "Host ip '"+ vm.host_ip + "' does not exist.")
            template_list = str(db.session.query(Template.id).filter(Template.id == vm.template_id).all())    # 检查是否存在该模板
            template_id = '('+str(vm.template_id)+'L,)'
            if template_id not in template_list:
                return render_template("vm/error.html",msg = "Template id " + str(vm.template_id) + " does not exists")
            vm_list = str(db.session.query(VM.vm_name).filter().all())    # 检查是否已存在该虚拟机
            vm_name = '(u\''+str(vm.vm_name)+'\',)'
            if vm_name in vm_list:
                return render_template("vm/error.html",msg = "VM name '"+ str(vm.vm_name) + "' already exist.")
            vm_info = db.session.query(Template.cpu, Template.memory, Template.disk, Template.image_id).filter(Template.id == vm.template_id).all()    # 获取模板的配置参数

            # 整理配置信息，创建虚拟机
            vm_cpu, vm_memory, vm_disk, vm_image_id = str(vm_info[0][0]),str(1024*vm_info[0][1]),str(vm_info[0][2]/1024)+'G',vm_info[0][3]
            vm_name = vm.vm_name
            vm_image_path = db.session.query(Image.image_path,Image.image_name).filter(Image.id==vm_image_id).all()    # 获取镜像路径
            if vm_image_path[0][0][-1] == '/':
                vm_image_path = vm_image_path[0][0] + vm_image_path[0][1]    # 镜像路径拼接
            else:
                vm_image_path = vm_image_path[0][0] + '/' + vm_image_path[0][1]
            vm_host_ip = vm.host_ip
            vm_instance = VM_Assistant(vm_name, vm_cpu, vm_memory, vm_disk, vm_image_path, vm_host_ip) # 根据虚拟机参数创建实例
            vm_instance.CreateVM()

            # 把虚拟机信息写入数据库
            vm.user_id = current_user.id
            vm.create_time = datetime.now()
            vm.vnc_port = vm_instance.GetVNCPort()
            vm.status = 'shut off'
            db.session.add(vm)
            db.session.commit()
        return redirect(url_for('vm.index'))

# 启动虚拟机
@vm.route('/launch/<int:vm_id>', methods = ['GET'])
@login_required
def launch(vm_id):
    vm = VM.query.filter(VM.id == vm_id).first()
    if vm and (vm.user_id == current_user.id or current_user.is_admin()):
        vm_instance = VM_Assistant(VMName=vm.vm_name, Host=vm.host_ip)
        host = Host.query.filter(Host.ip == vm.host_ip).first()
        try:
            vm_instance.LaunchVM()
        except:
            pass
        finally: 
            flash('Launch VM \'%s\' successfully.'%(vm.vm_name), 'success')
            vm.vnc_port = vm_instance.GetVNCPort()
            vm.status = get_vm_status(vm.vm_name, host)
            db.session.commit()
            open(vm, host)
        return redirect(url_for('vm.index'))
    else:
        return render_template("vm/error.html",msg = "You don't have permission to perform this operation.")

# 关闭虚拟机
@vm.route('/shutdown/<int:vm_id>', methods = ['GET'])
@login_required
def shutdown(vm_id):
    vm = VM.query.filter(VM.id == vm_id).first()
    if vm and (vm.user_id == current_user.id or current_user.is_admin()):
        vm_instance = VM_Assistant(VMName=vm.vm_name, Host=vm.host_ip)
        host = Host.query.filter(Host.ip == vm.host_ip).first()
        try:
            vm_instance.ShutdownVM()
        except:
            pass
        finally:
            flash('vm \'%s\' has been shutdown.'%(vm.vm_name), 'success')
            close(host)
            vm.status = get_vm_status(vm.vm_name, host)
            db.session.commit()
        return redirect(url_for('vm.index'))
    else:        
        return render_template("vm/error.html",msg = "You don't have permission to perform this operation.")

# 挂起虚拟机
@vm.route('/suspend/<int:vm_id>', methods = ['GET'])
@login_required
def suspend(vm_id):
    vm = VM.query.filter(VM.id == vm_id).first()
    if vm and (vm.user_id == current_user.id or current_user.is_admin()):
        vm_instance = VM_Assistant(VMName=vm.vm_name, Host=vm.host_ip)
        host = Host.query.filter(Host.ip == vm.host_ip).first()
        try:
            vm_instance.SuspendVM()
        except:
            pass
        finally:
            flash('VM \'%s\' has been suspended.'%(vm.vm_name), 'success')
            vm.status = get_vm_status(vm.vm_name, host)
            close(host)
            db.session.commit()
        return redirect(url_for('vm.index'))
    else:
        return render_template("vm/error.html",msg = "You don't have permission to perform this operation.")

# 恢复虚拟机
@vm.route('/resume/<int:vm_id>', methods = ['GET'])
@login_required
def resume(vm_id):
    vm = VM.query.filter(VM.id == vm_id).first()
    if vm and (vm.user_id == current_user.id or current_user.is_admin()):
        vm_instance = VM_Assistant(VMName=vm.vm_name, Host=vm.host_ip)
        host = Host.query.filter(Host.ip == vm.host_ip).first()
        try:
            vm_instance.ResumeVM()
        except:
            pass
        finally:
            flash('VM \'%s\' has been resumed.'%(vm.vm_name), 'success')
            vm.status = get_vm_status(vm.vm_name, host)
            open(vm, host)
            db.session.commit()
        return redirect(url_for('vm.index'))
    else:
        return render_template("vm/error.html",msg = "You don't have permission to perform this operation.")

# 删除虚拟机
@vm.route('/delete/<int:vm_id>', methods = ['GET'])
@login_required
def delete(vm_id):
    vm = VM.query.filter(VM.id == vm_id).first()
    if vm and (vm.user_id == current_user.id or current_user.is_admin()):
        vm_instance = VM_Assistant(VMName=vm.vm_name, Host=vm.host_ip)
        try:
            vm_instance.DeleteVM()
        except :
            pass
        finally:
            db.session.delete(vm)
            db.session.commit()
            flash('vm \'%s\' has been deleted.'%(vm.vm_name), 'success')
            return redirect(url_for('vm.index'))
    else:                
        return render_template("vm/error.html",msg = "You don't have permission to perform this operation.")

# 发现虚拟机
@vm.route('/discover')
@login_required
@admin_required
def discover():
    host_list = db.session.query(Host).filter().all()
    for i in range(len(host_list)): 
        host = host_list[i]
        vms_in_host = get_vm_list(host)    # 例如192.168.1.1中的虚拟机
        vms_in_db = [ str(i.vm_name) for i in VM.query.filter().all()]    # 数据库中的虚拟机
        for vm_name in vms_in_host:
            if vm_name not in vms_in_db:
                vm = VM()
                vm.vm_name = vm_name
                vm.host_ip = host.ip
                vm.create_time = datetime.now()
                vm.status = get_vm_status(vm.vm_name, host)
                vm.user_id = current_user.id    # 不存在数据库中的主机都归管理员所有
                vm.template_id = 0
                db.session.add(vm)
    db.session.commit()
    return redirect(url_for('vm.index'))
