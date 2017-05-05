import paramiko

def remote_control(ip, port, username, password, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username, password)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    res = stdout.read()
    ssh.close()
    return res

cmd = 'nohup /root/workspace/MyCloud/mycloud/virtscripts/noVNC/utils/launch.sh --vnc localhost:5900 &'
ip = '192.168.1.2'
username = 'root'
password = '123456'
port = 22

remote_control(ip, port, username, password, cmd)
