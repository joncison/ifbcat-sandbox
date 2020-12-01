# ifbcat

ifbcat is the database hosting and serving the IFB Catalogue through a REST API.

# How to contribute

## How code is formatted

Code is formatted using https://github.com/psf/black. Please use pre-commit along with black to commit only well formatted code:
```
#install dependencies
pip install -r requirements-dev.txt
#enable black as a pre-commit hook which will prevent committing not formated source
pre-commit install
#run black as it will be before each commit
pre-commit run black
```

## Run the API locally

1. Install requirements:

  * [docker](https://docs.docker.com/get-docker/),
  * [docker-compose](https://docs.docker.com/compose/install/),
  * postgresql-devel (libpq-dev in Debian/Ubuntu, libpq-devel on Centos/Cygwin/Babun.),
  * Virtual env,
  * requirements.txt

```
virtualenv .venv -p python3
. .venv/bin/activate
pip install -r requirements.txt
```

2. Run the DB locally:
```
# Copy (and optionally tweak) ini 
cp resources/default.ini local.ini
docker-compose run db
```

3. Retrieve data and run tests:
```
python manage.py test
```
Note this step requires read access to ifbcat-importdata. Currently, you should expect to see some "ERROR" but tests should be "OK" in the end of the log. 

4. Do migrations, superuser creation, some imports and start the test server
```
python manage.py migrate
python manage.py createsuperuser
python manage.py load_catalog
python manage.py runserver
```

5. You can do more imports using commands available in `ifbcat_api/management/commands`. Some are not currently working properly. Note that `load_catalog` should work.
```
python manage.py load_catalog
```

# How to manage the server

*All of this consider that you already are on the server and you are sudoer*

## Restart the service
```
sudo service ifbcat restart
```

## Pull the latest sources and restart
 * Restart stop the service, flush old images from disk, rebuild images and start the service. It clean up the server and helps in case of server full error 
```
cd /var/ifbcat-src
sudo git pull
sudo service ifbcat restart
```
 * Reload will rebuild the service before restarting it, it does not remove old image. It is faster
```
cd /var/ifbcat-src/ && sudo git pull && sudo service ifbcat reload
```
## Create a superuser
```
cd /var/ifbcat-src
sudo docker-compose exec web python manage.py createsuperuser
```

## Do some import
```
cd /var/ifbcat-src
sudo docker-compose run -v /var/ifbcat-importdata:/import_data web python manage.py load_persons /import_data/persons.csv /import_data/drupal_db_dump/users.txt
sudo docker-compose run -v /var/ifbcat-importdata:/import_data web python manage.py load_bioinformatics_teams /import_data/platforms.csv
sudo docker-compose run -v /var/ifbcat-importdata:/import_data web python manage.py load_biotools
```

Or all imports :
```
sudo docker-compose run -v /var/ifbcat-importdata:/code/import_data web python manage.py load_catalog
```

# How to generate graph models

To export the models to an image, you hav to:
 * uncomment django_extensions in settings.py
 * and then run this:
```bash
pip install pygraphviz django-extensions
python manage.py graph_models -a -g -o ifb_cat.png
python manage.py graph_models -a -g -o ifb_cat.svg
```
