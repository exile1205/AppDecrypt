import paramiko, re

class Worker(object):
    def __init__(self, hostname, username, password, workingDir=None, port=22):
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._connectArgs = { 
            'hostname': hostname,
            'username': username,
            'password': password,
            'port': port,
        }
        self._workingDir = workingDir


class AppDiscover(Worker):
    def getHexList(self):
        self._ssh.connect(**self._connectArgs)
        cmd = "ls /var/mobile/Applications"
        stdin, stdout, stderr = self._ssh.exec_command(cmd)
        list = [i.rstrip() for i in stdout.readlines()]
        self._ssh.close()
        list = filter(lambda x : re.search('^[A-Z0-9-]{36}$', x),list)
        return list
