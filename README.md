# Deployment-of-Item-Catalog-App
## Project Overview
This project take a baseline installation of a Linux server and prepare it to host Item-Catalog web application. Also, secure the server from a number of attack vectors, install and configure a database server, and deploy tem-Catalog application on it.
## Instructions for SSH access to the instance
   create account on any web hosting service such as AWS.
## Update all currently installed packages
    sudo apt-get update
    sudo apt-get upgrade
## Change the SSH port from 22 to 2200
Use `sudo vim /etc/ssh/sshd_config `
and then add Port 2200 under port 22 , (don't delete port 22 )save & quit.
Reload SSH using ` sudo service ssh restart`
## Configure the Uncomplicated Firewall (UFW)
Configure the Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123)

    sudo ufw allow 2200/tcp
    sudo ufw allow 80/tcp
    sudo ufw allow 123/udp
    sudo ufw enable 
 ## Connect to instance using ssh
 know you can acess the server from your termenal using the command 

    ssh -i .ssh/privetkey2.pem ubuntu@13.232.109.22 -p 2200
## Configure the local timezone to UTC
    sudo dpkg-reconfigure tzdata
## Create a new User grader
first in your local machine create a public and private keys using using any command line interface such as Git or Powershell (* my key name graderK)

    ssh key-gen 
then in your server creat the grader user `sudo adduser grader`
then 

    sudo mkdir /home/grader/.ssh 
    sudo touch /home/grader/.ssh/authorized_keys
then COPY GENERATED PUB KEY TO: `sudo nano authorized_keys`
then give him the sudo access

      touch /etc/sudoers.d/grader
      nano /etc/sudoers.d/grader
type in grader `ALL=(ALL:ALL) ALL `
save and quit
after that change some permissions to only allow grader user full access to files
  
    sudo chmod 700 /home/grader/.ssh
    sudo chmod 644 /home/grader/.ssh/authorized_keys 
    sudo chown -R grader:grader /home/grader/.ssh
    
then run ` service ssh restart`
try login with ` ssh grader@13.232.109.22 -p 2200 -i ~/.ssh/graderK `

## Block Root Login using SSH:
	sudo nano /etc/ssh/sshd_config

Modify the following line: `PermitRootLogin yes `
to : `PermitRootLogin no AllowUsers bionic grader`
then restart the ssh service `sudo service ssh restart`

## Install and configure Apache
Install Apache  ` sudo apt-get install apache2`
Install mod_wsgi `sudo apt-get install python-setuptools libapache2-mod-wsgi `
Restart Apache  `sudo service apache2 restart `
## Install and configure PostgreSQL
* Install PostgreSQL `sudo apt-get install postgresql`
* Check if no remote connections are allowed `sudo nano /etc/postgresql/9.5/main/pg_hba.conf`
* Login as user "postgres" `sudo su - postgres`
* Get into postgreSQL shell: `psql`
* Create a new database named catalog  and create a new user named catalog in postgreSQL shell

      postgres=# CREATE DATABASE catalog;
      postgres=# CREATE USER catalog;

** Set a password for user catalog which is **123456**
	
	postgres=# ALTER ROLE catalog WITH PASSWORD '123456';
	
* Give user "catalog" permission to "catalog" application database
	
	  postgres=# GRANT ALL PRIVILEGES ON DATABASE catalog TO catalog;

* Quit postgreSQL `postgres=# \q`
* Exit from user "postgres" `exit`
 
## Install git, clone and setup your Catalog App project.
* Install Git using `sudo apt-get install git`
* Create a folder catalog under the /var/www directory 

      cd /var/www sudo mkdir catalog
      cd catalog
* Clone the Item-catalog App to the catalog directoy and name it Item-Catalog as  following

      clone https://github.com/alia55/Deployment-of-Item-Catalog-App.git Item-Catalog
## Install and Set up Flask and Virtual Environment
    sudo apt-get install python-pip 
    sudo pip install virtualenv
    sudo virtualenv venv 
    source venv/bin/activate 
    sudo chmod -R 777 venv 
## Installing Dependencies:
after activating the environment install all the dependecies

      sudo python2 -m pip install sqlalchemy
      sudo python2 -m pip install flask
      sudo python2 -m pip install psycopg2-binary
      sudo python2 -m pip install Pillow
      sudo -H python2 -m pip install oauth2client
      
## Configure and Enable a New Virtual Host 
* Create FlaskApp.conf to edit: `sudo nano /etc/apache2/sites-available/FlaskApp.conf`
* Add the following lines of code to the file to configure the virtual host. 	

      <VirtualHost *:80>
                    ServerName 13.232.109.22.xip.io
                   ServerAdmin 13.232.109.22
                   WSGIDaemonProcess catalog python-path=/var/www/catalog:/var/www/catalog/venv/lib/python2.7/site-packages
                   WSGIProcessGroup catalog
                   WSGIScriptAlias / /var/www/catalog/flaskapp.wsgi
                   <Directory /var/www/catalog/Item-Catalog/>
                           Order allow,deny
                           Allow from all
                   </Directory>
                   Alias /static /var/www/catalog/Item-Catalog/static
                   <Directory /var/www/catalog/Item-Catalog/static/>
                           Order allow,deny
                           Allow from all
                   </Directory>
                   ErrorLog ${APACHE_LOG_DIR}/error.log
                   LogLevel warn
                   CustomLog ${APACHE_LOG_DIR}/access.log combined
       </VirtualHost>

* Enable the virtual host with the following command: `sudo a2ensite FlaskApp`

## Create the .wsgi File :
* Create the .wsgi File under /var/www/FlaskApp: 

      cd /var/www/FlaskApp
      sudo nano flaskapp.wsgi 
	
* Add the following lines of code to the flaskapp.wsgi file:(Replace 'ADD YOUR SECRET KEY HERE' with your key)

      #!/usr/bin/python
      import sys
      import logging
      logging.basicConfig(stream=sys.stderr)
      sys.path.insert(0,"/var/www/catalog/Item-Catalog")

      from __init__ import app as application
      application.secret_key = 'ADD YOUR SECRET KEY HERE'

## Restart Apache:
* Restart Apache`sudo service apache2 restart `

* Then go to browser and type [13.232.109.22.xip.io](http://13.232.109.22.xip.io) :trophy:

 
  
