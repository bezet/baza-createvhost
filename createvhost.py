#!/usr/bin/python

import sys, getopt


def main(argv):
	hostsFile = open('C:/Windows/System32/drivers/etc/hosts', 'a')
	httpdHostsFile = open('C:/wamp/bin/apache/apache2.4.9/conf/extra/httpd-vhosts.conf', 'a')
	newVHost = argv[0]
	projectDir = argv[1]

	if newVHost.rfind('.') == -1:
		newVHost = newVHost + '.local'
		
	print('Creating new virtual host:', newVHost)
	
	hostsFile.write('\n' + '127.0.0.1       ' + newVHost)

	# <VirtualHost *:80>
	# 	ServerName baza.local
	# 	ServerAlias baza.local
	# 	DocumentRoot "C:/wamp/www/git/portfolio"
	# 	<Directory "C:/wamp/www/git/portfolio/">
	# 		Options Indexes FollowSymLinks MultiViews
	# 		AllowOverride all
	# 		Require all granted
	# 		Require local
	# 	</Directory>
	# </VirtualHost>
	
	vhostDef = [
		'  <VirtualHost *:80>',
		'    ServerName ' + newVHost,
		'    ServerAlias ' + newVHost,
		'    DocumentRoot "'+ projectDir +'"',
		'    <Directory "'+ projectDir +'/">',
		'      Options Indexes FollowSymLinks MultiViews',
		'      AllowOverride all',
		'      Require all granted',
		'      Require local',
		'    </Directory>',
		'  </VirtualHost>',
	]

	vhostDef = '\n'.join(vhostDef)
	
	httpdHostsFile.write('\n\n' + vhostDef)
	
	hostsFile.close()
	httpdHostsFile.close()

	print('Done!')
	print('Project\'s directory:', projectDir)
	print('Your new url:', 'http://' + newVHost)


if __name__ == "__main__":
   main(sys.argv[1:])