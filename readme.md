## APP Decrypt

App Decrypt tool uses in AppBeach

The decrypted library use [dumpdecrypted](https://github.com/stefanesser/dumpdecrypted) from Stefan Esser.

### Requirement

##### Computer

PC run an unix-Like operating system.

Python 2.7 is required.

On OS X, you can install it simply by typing ‘otool’, ‘lipo’ and following the prompt window to install these command lines tools if you had XCode installed. 

On Linux, you can follow the instructions on this repository to build a runnable cctools for Linux / FreeBSD from [source] (https://github.com/tpoechtrager/cctools-port). 

The decrypter uses some third-party Python modules, and you need to install them on you system. paramiko and biplist is required Python modules to run the decrypter. 

Using virtualenv is a good idea since it creates separate and isolated Python environments for each project, without affecting your system. If you’re using easy_install or pip, you might need to install python development package since paramiko contains part of code required to compile is written in C, and you shall have file command installed on your machine, too.


##### iDevice

A jailbroken iOS device(iPod Touch, iPhone, iPad) which install Cydia where user can find out the packages list below.

First, install the __openssh__ package to be able to ssh the iDevice. Second, install __MobileTerminal__ package to change ssh password, which default is *alpine* Changing the password, to get higher security. Final, install __File__ package to get __File__ command in terminal which is an important function would be used in code.

After installing those, you can access iDevice with ssh portal. Then put the [dumpdecrypted](https://github.com/stefanesser/dumpdecrypted) into home directory from iDevice

### Connecttin to iDevice

##### WiFi

After installing __openssh__ package from Cydia, user can try to build a ssh connect to iDevice. Use a computer which connects to a Wi-Fi same as iDevice, and then check the Wi-Fi IP in the iDevice. User can get that information by clicking the connect WiFi from iDevice. Finally, open a terminal window and then type the login command below.

	ssh root@[IP address from iDevice]

##### USB Cable

If you want to access your iDevice over USB cable instead of WiFi, you shall have usbmuxd built and installed on your system. After that, Unplug, replug your device, and fire up a terminal typing:

	iproxy 2222 22

Don’t interpret the command, and all traffic to port 2222 on your machine will redirect to port 22 of your device. So a standard SSH login prompt will be like this:
 
	ssh -p 2222 root@localhost

### Setting

Setting file is under src/setting.py

	iDevice =	{
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

Enter command to run python virtual environments.

	source env/bin/activate

Enter command to run python code.

	python src/do.py
	
The code would make directory under the output_dir which is parameter from setting.py.
	

### Output

Binary file will export under __output_dir/binary__

Decrypt file will export under __output_dir/decrypt__

Armv7 file will export under __output_dir/armv7__

Armv7s file will export under __output_dir/armv7s__

Json file will export under __output_dir/json__
