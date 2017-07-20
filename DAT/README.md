Get the apache web server to run python scripts:
--------------------
sudo apt-get update

sudo apt-get install apache2

sudo mkdir /var/www/pythonApi

sudo chmod 755 /var/www/pythonApi/

sudo vi /etc/apache2/sites-available/000-default.conf 

        DocumentRoot /var/www
        <Directory "/var/www/pythonApi">
           AddHandler cgi-script .py
           Options +Indexes +ExecCGI
           DirectoryIndex index.py
           AllowOverride Limit
        </Directory>

sudo a2enmod cgi

echo "ServerName localhost" | sudo tee /etc/apache2/conf-available/servername.conf

sudo service apache2 restart 

Install pdfminer used for parsing and converting PDF files:
--------------------
sudo apt-get install git

sudo git clone https://github.com/euske/pdfminer.git

cd pdfminer/

sudo python setup.py install

Install NLTK(Natural language Processing) used as the project backbone:
--------------------------
sudo apt-get update

sudo git clone https://github.com/nltk/nltk.git

cd nltk/

sudo python setup.py install


Download the files from the git and unzip them into /var/www/
-----------------
set the scrawl script to run like a cron job once in every 24 hours. (OPTIONAL: required when you need refreshed new data)
----------------
restart the apache
-------------
load the webpage from http://localhost/dat.html
-------------------
start using the App. The app is responsive and can be used in phones, iPads and desktops.
-----------------

