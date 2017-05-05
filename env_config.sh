#!/bin/bash
#
apt-get update
apt-get install -y libmysqlclient-dev python-dev
apt-get upgrade -y python
apt-get install -y python-pip
apt-get install -y python-virtualenv
virtualenv venv
source venv/bin/activate
#
pip install flask
pip install flask-wtf
pip install flask-cache
pip install flask-login
pip install flask-script
pip install flask-migrate
pip install mysql-python
pip install paramiko
pip install pycrypto ecdsa
#
apt-get install -y qemu
apt-get install -y libvirt-bin python-libvirt
cp /usr/lib/python2.7/dist-packages/libvirt* /root/workspace/MyCloud/venv/lib/python2.7/site-packages
apt-get install -y tightvncserver
apt-get install -y git
git clone https://github.com/kanaka/noVNC
#
apt-get install -y mysql-server


#
pip freeze > requirements.txt
