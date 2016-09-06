#!/usr/bin/python

import os, sys, getopt, json
# import subprocess, webbrowser


def createConfigFile(configPath):

    config = [
        '{',
        '   "hostsFile": "C:/Windows/System32/drivers/etc/hosts",',
        '   "httpdHostsFile": "C:/wamp64/bin/apache/apache2.4.18/conf/extra/httpd-vhosts.conf"',
        '}'
    ]

    config = '\n'.join(config)

    configFile = open(configPath, 'w')
    configFile.write(config)
    configFile.close()

    print("Provide paths to your hosts and httpd-vhosts.conf files.")
    editFile(configPath)


def editFile(filePath, editor="notepad.exe"):
    
    # webbrowser.open(filePath)
    # subprocess.Popen([editor, filePath])
    os.system(editor + " " + filePath)


def createVirtualHost(hostsFile, httpdHostsFile, hostname, projectDirectory):
    
    hostsFile.write('\n' + '127.0.0.1       ' + hostname)

    ## This is a working example of vhost, just in case  
    # <VirtualHost *:80>
    #   ServerName virtualhost.local
    #   ServerAlias virtualhost.local
    #   DocumentRoot "C:/wamp/www/virtualhostdir"
    #   <Directory "C:/wamp/www/virtualhostdir/">
    #       Options Indexes FollowSymLinks MultiViews
    #       AllowOverride all
    #       Require all granted
    #       Require local
    #   </Directory>
    # </VirtualHost>
    
    vhostDef = [
        '  <VirtualHost *:80>',
        '    ServerName ' + hostname,
        '    ServerAlias ' + hostname,
        '    DocumentRoot "' + projectDirectory + '"',
        '    <Directory "' + projectDirectory + '/">',
        '      Options Indexes FollowSymLinks MultiViews',
        '      AllowOverride all',
        '      Require all granted',
        '      Require local',
        '    </Directory>',
        '  </VirtualHost>',
    ]

    vhostDef = '\n'.join(vhostDef)
    
    httpdHostsFile.write('\n\n' + vhostDef)


def usage():
    
    usageText = [
        ' ',
        'usage:',
        '    python ' + sys.argv[0] + ' [-c | --config] [[-n | --name=<hostname>] [-d | --directory=<project-directory>]]',
        ' ',
        'examples:',
        '    python ' + sys.argv[0] + ' --config',
        '        Pops up notepad.exe with Windows hosts & HTTP server vhosts config (vhosthttpd-vhosts.conf) filepaths configuration.',
        ' ',
        '    python ' + sys.argv[0] + ' --config --name newhostname --directory C:/project',
        '        Configure paths and set up a new local virtual host. If you provide a name without dot, .local is added to the final url.',
        ' ',
        '    python ' + sys.argv[0] + ' --name newhostname --directory C:/project',
        '        If configuration is already done, it simply sets up a new virtual host. If config doesn\'t exist, notepad.exe pops up anyway.'
    ]

    usageText = '\n'.join(usageText)

    print(usageText)


def main(argv):

    if len(argv) == 0:
        print("Rerun script with apropriate options and arguments.")
        usage()
        sys.exit()

    try:
        opts, args = getopt.getopt(argv, 'hcn:d:', ['help', 'config', 'name=', 'directory='])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    scriptDirectory = os.path.dirname(os.path.abspath(__file__))
    configPath = os.path.join(scriptDirectory, 'config.json')

    hostname = None
    projectDirectory = None

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()

        if opt in ('-c', '--config'):
            if not os.path.isfile(configPath):
                createConfigFile(configPath)
            else:
                editFile(configPath)

            print("Config is set.")

        if opt in ('-n', '--name'):
            if len(arg) > 0:
                hostname = arg

                if hostname.rfind('.') == -1:
                    hostname = hostname + '.local'
            else:
                print("Name option value is empty.")
                sys.exit()

        if opt in ('-d', '--directory'):
            if os.path.isdir(arg):
                projectDirectory = arg
            else:
                print("Provided directory path doesn't exist. Make sure it's valid or create directory first and rerun the script.")
                sys.exit()

    if hostname is None or projectDirectory is None:
        print("You're doing it wrong.")
        usage()
        sys.exit()

    if not os.path.isfile(configPath):
        createConfigFile(configPath)

    while 1:
        try:
            with open(configPath) as configFile:
                config = json.load(configFile)

            hostsFile = open(config['hostsFile'], 'a')
            httpdHostsFile = open(config['httpdHostsFile'], 'a')

            print("Config is set.")
            break

        except FileNotFoundError:
            keyInput = input("File paths provided in your config are invalid - do you want to edit config file? y/n \n")

            if keyInput == 'y' or keyInput == 'yes':
                editFile('config.json')
            elif keyInput == 'n' or keyInput == 'no':
                sys.exit()
        
    print('Creating a new virtual host:', hostname)
    createVirtualHost(hostsFile, httpdHostsFile, hostname, projectDirectory)
    
    hostsFile.close()
    httpdHostsFile.close()

    url = 'http://' + hostname

    print("Done!")
    print("Project's directory:", projectDirectory)
    print("Your new url:", url)
    print("You might need to restart your HTTP server.")

    # webbrowser.open(url)


if __name__ == "__main__":
    main(sys.argv[1:])