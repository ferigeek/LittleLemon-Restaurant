import os
import subprocess
import datetime
from pathlib import Path


try:
    # requirements installation
    subprocess.run("sudo apt update && sudo apt upgrade -y", shell=True)
    subprocess.run("sudo apt install libapache2-mod-wsgi-py3 -y", shell=True)
    subprocess.run("sudo apt install python3-dev -y", shell=True)
    subprocess.run("sudo apt install build-essential -y", shell=True)
    subprocess.run("sudo apt install libmysqlclient-dev -y", shell=True)
    subprocess.run("sudo apt install pkg-config -y", shell=True)
    subprocess.run("sudo apt install apache2 -y", shell=True)
    subprocess.run("sudo apt install mysql-server -y", shell=True)
    subprocess.run("sudo apt install python3-venv -y", shell=True)
    
    # Domain
    domain = input("Enter the domain address of you application: ")
    alias = input("Enter the alias for your domain (Just press enter if you don't want any): ")
    
    # Virtual environment creation
    subprocess.run("cd .. && python3 -m venv env", shell=True)
    subprocess.run("source ../env/bin/activate && pip install -r ../req.txt", shell=True)

    # Apache Configuration
    print("Creating apache config ...")

    with open(r"/etc/apache2/sites-available/littlelemon.conf", 'w') as conf:
        conf.write(r"<VirtualHost *:443>")
        conf.write(f"\tServerName {domain}")
        if alias == None:
            conf.write(f"\tServerAlias {alias}")
        conf.write(f"\nDocumentRoot {Path.cwd().parent}\n")
        conf.write(f"\tWSGIDaemonProcess littlelemon python-path={Path.cwd().parent}:{Path.cwd().parent}/env/lib/python3.12/site-packages")
        conf.write("\tWSGIProcessGroup littlelemon")
        conf.write(f"\tWSGIScriptAlias / {Path.cwd().parent}/littlelemon/wsgi.py")
        conf.write(f"\n\t<Directory {Path.cwd().parent}")
        conf.write("\t\t<Files wsgi.py>\n\t\t\tRequire all granted\n\t\t</Files>\n</Directory>")
        conf.write(f"\nAlias /static {Path.cwd().parent}/static")
        conf.write(f"<Directory {Path.cwd().parent}/static>\n\t\tRequire all granted\n\t</Directory>")
        conf.write(f"\nAlias /media {Path.cwd().parent}/media")
        conf.write(f"<Directory {Path.cwd().parent}/media>\n\t\tRequire all granted\n\t</Directory>")
        r_domain = str()
        for i in range(len(domain), -1, -1):
            if domain[i] == '.':
                r_domain = domain[:i] + '\\' + domain[i:]
                break
        conf.write("RewriteEngine On\n" + r"RewriteCond %{HTTP_HOST} ^" + r_domain + " [NC]")
        conf.write(r"RewriteRule ^(.*)$ https://" + domain + r"/$1 [L,R=301]")
        conf.write(r"\nErrorLog ${APACHE_LOG_DIR}/error-littlelemon.log")
        conf.wrtie(r"CustomLog ${APACHE_LOG_DIR}/access-littlelemon.log combined")
        conf.write(r"</VirtualHost>")
    content = list()

    # settings.py
    print('Configuring settings.py ...')
    with open('../littlelemon/settings.py', '+a') as settings:
        settings.write('CSRF_COOKIE_SECURE = True')
        settings.write('SESSION_COOKIE_SECURE = True')
        settings.write('SECURE_HSTS_SECONDS = True')
        settings.write('SECURE_SSL_REDIRECT = True')
        content = settings.readlines()
        for i in range(len(content)):
            if content[i] == "DEBUG = True":
                content[i] = "DEBUG = False"
                break
    with open('../littlelemon/settings.py', 'w') as settings:
        settings.writelines(content)
    
    # Environment variables
    print("Configuring environment variables ...")
    secret_key = input("Enter secret key for your application: ")
    db_name = input("Enter the database name to create: ")
    db_username = input("Enter the database username: ")
    db_password = input("Enter the database password: ")

    with open('../.env', '+a') as env:
        env.write("DATABASE_ENGINE=django.db.backends.mysql")
        env.write("DATABASE_NAME="+db_name)
        env.write("DATABASE_USER="+db_username)
        env.write("DATABASE_PASS="+db_password)
        env.write("DATABASE_HOST=127.0.0.1")
        env.write("DATABASE_PORT=3306")
    
    # authorization
    subprocess.run(f"sudo chown -R www-data:www-data {Path.cwd().parent}", shell=True)
    subprocess.run(f"sudo chmod -R 755 {Path.cwd().parent}", shell=True)
    subprocess.run(f"sudo chmod o+x /home", shell=True)
    subprocess.run(f"sudo chmod o+x /home/{os.getlogin()}", shell=True)

    # SSL
    subprocess.run("sudo apt install python3-certbot-apache", shell=True)
    subprocess.run(f"sudo certbot --apache -d {domain} -d {alias}", shell=True)

    subprocess.run("sudo mysql_secure_installation", shell=True)
    subprocess.run(f"mysql -u root -p && CREATE USER \'{db_username}\'@\'localhost\' IDENTIFIED BY \'{db_password}\';\
                && CREATE DATABASE {db_name}; && GRANT ALL PRIVILEGES ON {db_name}.* TO '{db_username}'@'localhost';\
                    && FLUSH PRIVILEGES;", shell=True)
    
    subprocess.run("sudo a2ensite littlelemon.conf", shell=True)
    subprocess.run("sudo systemctl restart apache2", shell=True)
    print("Done!")
except Exception as ex:
    print(ex)