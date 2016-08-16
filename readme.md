Script creating local virtual hosts (Windows 7, Apache)

usage:
	python createvhost.py [-c | --config] [[-n | --name=<hostname>] [-d | --directory=<project-directory>]]

examples:
	python createvhost.py --config
	    Pops up notepad.exe with Windows hosts & web server vhosts config (vhosthttpd-vhosts.conf) filepaths configuration.
         
	python createvhost.py --config --name newhostname --directory C:/project
	    Configure paths and set up a new virtual host. If you provide name without dot, .local is added to the final url.
         
	python createvhost.py --name newhostname --directory C:/project
        If configuration is already done, it simply sets up a new virtual host. If config doesn\t exist, notepad.exe pops up anyway.
