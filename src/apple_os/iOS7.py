from Utils import Worker

from jinja2 import Environment, FileSystemLoader
import biplist
import paramiko
import re
import os
import json
import shutil
import io
import subprocess
from bson import json_util


class iDeviceWorker(Worker):
    itemId = None
    itemName = None
    binary_path = None
    file_binary_path = None
    is_binary_exists = None
    binary_filename = None
    genre = None
    targetDir = "./"

    def assignLongHexKey(self, long_hex_key):
        self.__long_hex_key = long_hex_key

    def setItemId_and_getPlistDict(self):
        try:
            self._ssh.connect(**self._connectArgs)
            cmd = 'cat /var/mobile/Applications/%s/iTunesMetadata.plist' % self.__long_hex_key
            stdin, stdout, stderr = self._ssh.exec_command(cmd)
            #bPlist = stdout.read()
            # print bPlist
            bPlist = ''.join(stdout.read())
            self._ssh.close()
            PlistDict = biplist.readPlistFromString(bPlist)
            self.itemName = PlistDict[u'itemName']
            self.itemId = PlistDict['itemId']
            self.genre = PlistDict['genre']
        except:
            print "Fail, Maybe it is a Built-in App without metadata."
            find_com = 'find /var/mobile/Applications/%s/*.app' % self.__long_hex_key
            self._ssh.connect(**self._connectArgs)
            stdin, stdout, stderr = self._ssh.exec_command(find_com)
            stdout = ''.join(stdout.read())
            print 'This app is %s' % stdout.split('/')[-1]
            self._ssh.close()
            PlistDict = {}
        return PlistDict

    def findBin(self):
        if not self.__long_hex_key:
            return -1
        filetype = ['Mach-O fat file with 2 architectures',
                    'Mach-O executable acorn']
        #filetype = ['Mach-O fat file with 2 architectures']
        self._ssh.connect(**self._connectArgs)
        cmd = 'cat /var/mobile/Applications/%s/*.app/Info.plist'
        stdin, stdout, stderr = self._ssh.exec_command(
            cmd % self.__long_hex_key)
        bPlist = ''.join(stdout.read())
        PlistDict = biplist.readPlistFromString(bPlist)
        exetuable_name = PlistDict['CFBundleExecutable']
        if(" " in exetuable_name):
            exetuable_name = exetuable_name.replace(" ", "\ ")

        getfilebinPath = "cd /var/mobile/Applications/%s/*.app/ && echo $(pwd)/%s" % (
            self.__long_hex_key, exetuable_name)
        stdin, stdout, stderr = self._ssh.exec_command(getfilebinPath)
        filebinPath = ''.join(stdout.read()).rstrip()
        stdin, stdout, stderr = self._ssh.exec_command(
            "file '%s'" % filebinPath)
        checkfile = ''.join(stdout.read())
        binPath = filebinPath
        if(" " in filebinPath):
            binPath = filebinPath.replace(" ", "\ ")
        for i in filetype:
            if i in checkfile:
                self.binary_path = binPath
                self.file_binary_path = filebinPath
                self.is_binary_exists = True
        self._ssh.close()

    def getOriginalBin(self):
        self._ssh.connect(**self._connectArgs)
        sftp = self._ssh.open_sftp()
        original_target_path = self.targetDir + 'binary/'
        target_path = '%s%s' % (original_target_path, self.itemId)
        #if not os.path.exists(target_path): os.makedir(target_path)

        sftp.get(self.file_binary_path, target_path)
        sftp.close()
        self._ssh.close()
        print "get OriginalBin succeed"
        return target_path

    def doDecrypted(self):
        self._ssh.connect(**self._connectArgs)
        dec_command = 'DYLD_INSERT_LIBRARIES=dumpdecrypted.dylib %s mach-o decryption dumper' % (
            self.binary_path)
        stdin, stdout, stderr = self._ssh.exec_command(dec_command)
        print "Decrypted done"
        self._ssh.close()

    def checkDecryptedBin(self):
        binary_filename = self.binary_path.split('/')[-1]
        print "checking DecryptBinary"
        print binary_filename
        if ("\ " in binary_filename):
            self._ssh.connect(**self._connectArgs)
            newbinary_filename = binary_filename.replace("\ ", "")
            mv_command = 'mv %s.decrypted %s.decrypted' % (
                binary_filename, newbinary_filename)
            stdin, stdout, stderr = self._ssh.exec_command(mv_command)
            print "rename done"
            self.binary_filename = newbinary_filename
            self._ssh.close()
        else:
            self.binary_filename = binary_filename

    def getDeBin(self):

        de_path = '%s.decrypted' % self.binary_filename
        print de_path
        target_path = '%s%s' % (self.targetDir, self.itemId)
	
	self._ssh.connect(**self._connectArgs)
        sftp = self._ssh.open_sftp()
        sftp.get(de_path, target_path)
        sftp.close()
        self._ssh.close()
	armv7_target_path = '%sarmv7/%s.armv7' % (self.targetDir, self.itemId)
        shutil.copy(target_path, armv7_target_path)

        command = "arm-apple-darwin11-lipo -thin armv7 " + str(self.itemId) + " -output armv7/" + str(self.itemId) + ".armv7"

        subprocess.call(command, shell=True)

        move_path =  '%sdecrypted/%s' % (self.targetDir, self.itemId)
        shutil.move(target_path, move_path)
        print "Get decrypted %s succeed" % self.itemName
        return target_path

    def rmDeBin(self):
        self._ssh.connect(**self._connectArgs)
        binary_filename = self.binary_path.split('/')[-1]
        de_path = '%s.decrypted' % self.binary_filename
        rm_command = 'rm %s' % de_path
        stdin, stdout, stderr = self._ssh.exec_command(rm_command)
        print "Removed %s.decrypted succeed" % self.itemName
        self._ssh.close()


class LinuxWorker(object):

    def __init__(self, binpath):
        self.binpath = binpath

    def doDD(self, offset, cryptoff, cryptsize, vmaddr, addr):
        seek = int(offset) + int(cryptoff)
        count = cryptsize
        cmd = 'dd bs=1 conv=notrunc if="%s.decpart" of="%s" skip=0 seek=%s count=%s' % (
            self.binpath, self.binpath, seek, count)
        if os.system(cmd) == 0:
            os.remove('%s.decpart' % self.binpath)
            return self.binpath

    def getBinInfo(self):
        i = self.binpath
        cmd = 'arm-apple-darwin11-otool -f "%s" | grep -A 2 "cpusubtype 9" && arm-apple-darwin11-lipo -thin armv7 "%s" -output "%s.armv7" && arm-apple-darwin11-otool -l "%s.armv7" | grep LC_ENCRYPTION -A 4 | grep crypt && arm-apple-darwin11-otool -l "%s.armv7" | grep __TEXT -A 3 -B 1 | head -12 | grep addr && rm "%s.armv7"' % (
            i, i, i, i, i, i)
        stdout = [i for i in os.popen(cmd)]

        # Transform to a dictionary as **kargs purpose
        info = {
            'offset': None,
            'cryptoff': None,
            'cryptsize': None,
            'vmaddr': None,
            'addr': None,
        }

        for i in info.keys():
            for k in stdout:
                if re.search('^\s{0,}%s' % i, k):
                    info[i] = k.replace(i, "").replace(" ", "").rstrip()
        return info

    def getPair(self, PlistDict):
        self.itemID = str(PlistDict['itemId'])

        try:
            content = json.dumps(PlistDict, default=json_util.default)
        except(TypeError, ValueError) as err:
            print 'ERROR:', err
        pList = open('%s.plist.json' % self.binpath, 'w')
        pList.write(content)
        pList.close()
        jsonPath = '%s.plist.json' % self.binpath
	move_path =  '%sjson/%s' % (self.targetDir, jsonPath)
        shutil.move(jsonPath, jsonNewPath)
        print 'json done'
