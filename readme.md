## APP Decrypt

App Decrypt tool uses in AppBeach

The decrypted library use [dumpdecrypted](https://github.com/stefanesser/dumpdecrypted) from Stefan Esser.

### Requirement

##### Computer

PC running a Unix-Like operating system.

Python 2.7 is required.

On OS X, you can install it simply by typing ‘otool’, ‘lipo’ and following the prompt window to install these command lines tools if you had XCode installed. 

On Linux, you can follow the instructions on this repository to build a runnable cctools for Linux / FreeBSD from [source] (https://github.com/tpoechtrager/cctools-port). 

The decrypter uses some third-party Python modules, and you need to install them on you system. paramiko and biplist is required Python modules to run the decrypter. 

Using virtualenv is a good idea since it creates separate and isolated Python environments for each project, without affecting your system. If you’re using easy_install or pip, you might need to install python development package since paramiko contains part of code required to compile is written in C, and you shall have file command installed on your machine, too.


##### iDevice

A jailbroken iOS device(iPod Touch, iPhone, iPad) which install Cydia, terminal, openssh.

After installing, you can access iDevice with ssh portal. Then put the [dumpdecrypted](https://github.com/stefanesser/dumpdecrypted) into home directory from iDevice

##### USB Connect

If you want to access your iDevice over USB cable instead of WiFi, you shall have usbmuxd built and installed on your system. After that, Unplug, replug your device, and fire up a terminal typing:

	$ ./iproxy 2222 22

Don’t interpret the command, and all traffic to port 2222 on your machine will redirect to port 22 of your device. So a standard SSH login prompt will be like this:
 
	$ ssh -p 2222 root@localhost

### Setting

Setting file is under src/setting.py

	iPad =	{
		'username': #iDevice ssh account
		'password': #iDevice ssh password
		'hostname': #iDevice ssh hostname
		'port': #ssh port
	}
	
	ftp = {
		 'username': #ftp username
	    'password': #ftp password
	    'hostname': #ftp hostname
	    'port': #ftp port
	}
	
	output_dir = # output dir

### Sample usage

Enter command to run python virtual environments

	source env/bin/activate

Enter command to run python code.

	python src/do.py
	

### Output

Binary file will export under __output_dir/binary__

Decrypt file will export under __output_dir/decrypt__

Armv7 file will export under __output_dir/armv7__

Json file will export under __output_dir/json__