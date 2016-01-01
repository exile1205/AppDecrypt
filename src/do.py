from apple_os.Utils import AppDiscover
from apple_os import iOS9
import os, ftplib, json
import settings

app = AppDiscover(**settings.iDevice)

def writeIntoDownloadLog(PLIST):
    itemId = PLIST[u'itemId']
    appName = PLIST[u'itemName']
    genreId = PLIST[u'genreId']
    genreName = PLIST[u'genre']
    logfile = open("/Home/soslab/download_log", "a")
    text = "[%s] %s %s %s\n" % (genreName.encode("utf8"), genreId, itemId, appName.encode("utf8"))
    logfile.write(text)
    logfile.close()

def uploadFileToServer(PLIST_FILE_PATH, EXECUTABLE_FILE_PATH, PlistDict):
    ftp_args = {
        'host': settings.ftp['hostname'],
        'user': settings.ftp['username'],
        'passwd': settings.ftp['password'],
    }
    session = ftplib.FTP(**ftp_args)
    plist_file = open(PLIST_FILE_PATH, 'rb')
    executable = open(EXECUTABLE_FILE_PATH, 'rb')
    print 'Sending files to server......'
    session.storbinary('STOR %s' % plist_file.name.split("/")[-1], plist_file)
    session.storbinary('STOR %s' % executable.name.split("/")[-1], executable)
    plist_file.close()                                    # close file and FTP
    executable.close()
    session.quit()
    print "Files Sent to Server: OKAY"
    os.remove(PLIST_FILE_PATH)
    os.remove(EXECUTABLE_FILE_PATH)
    writeIntoDownloadLog(PlistDict)
def createOutputFolder():
    folderList = ['armv7', 'armv7s', 'binary', 'decrypted', 'json']
    for folder in folderList:
	checkingFolder = settings.output_dir + folder
        if not os.path.exists(checkingFolder):
	    os.makedirs(checkingFolder)
	    print "The folder %s is created" % checkingFolder
def decrypt(hex):
    print "---------------------------------------------------"
    print " Decrypting app %s" % hex
    ios_worker = iOS9.iDeviceWorker(**settings.iDevice)
    ios_worker.assignLongHexKey(hex)
    PlistDict = ios_worker.setItemId_and_getPlistDict()
    print "The app is %s" % PlistDict[u'itemName']
    ios_worker.findBin()
    if ios_worker.binary_path is not None:
        ios_worker.targetDir = settings.output_dir
        localBinPath = ios_worker.getOriginalBin()
        linux_worker = iOS9.LinuxWorker(localBinPath)
	print "%s Decrypting Start"% PlistDict[u'itemName']
	ios_worker.doDecrypted() 
	ios_worker.checkDecryptedBin()       
	ios_worker.getDeBin()
	print "Clear decrypted file in iDevice."
	ios_worker.rmDeBin()
	print "Retrieve metadata as json file."
        #if decpart_path is not None:
            #bin_path = linux_worker.doDD(**dec_dict)
	#print PlistDict
        linux_worker.getPair(PlistDict)
	print "%s has been finished."% PlistDict[u'itemName']
        # uploadFileToServer('%s.plist.json' % bin_path, bin_path, PlistDict)
	#print "Uploaded"
        #else:
        # print "Decryption failed on %s" % hex
    else:
        print "App skiped: %s,because it is not 'Mach-O fat file with 2 architectures' or 'Mach-O executable acorn'." % hex    

if __name__ == "__main__":
    app = AppDiscover(**settings.iDevice)
    createOutputFolder();
    for i in app.getHexList():       
	try:
            decrypt(i)
            #print "---------------------------------------------------"
        except KeyboardInterrupt:
            print "Good-Bye!"
            break
        except:
            pass
