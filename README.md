# Django Deployment on Heroku

This project is for explaining how to deploy a local django project with sqlite3 from Windows 7 64bits on Heroku. Heroku does not support sqlite3 because its filesystem is ephemeral. A PostgreSQL db is created on production instead. A local PostgreSQL server has to be installed for db data pushing.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
See deployment for notes on how to deploy the project on heroku system.


### Prerequisites (All the packages are for Windows 7 Ultimate 64 bits)

PostgreSQL 11.05

https://get.enterprisedb.com/postgresql/postgresql-11.5-1-windows-x64.exe

Python 3 (Python 3.6.8)

https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64.exe

pip 9.0.3

virtualenv 16.7.4

dj-database-url 0.5.0

Django 2.2.4

gunicorn 19.9.0

psycopg2 2.7.4

python-decouple 3.1

pytz 2019.2

sqlparse 0.3.0

whitenoise 4.1.3

### Installing


### PostgreSQL

It is not recomended to install in the default location which is ProgramFiles since this will place your database files in the Progams directory as well.

If the installer fails durring the C++ 2013 runtime install, you probably already have a version of C++ 2013.
You can solve this issue by openening a cmd window in your installer directory and enter:
postgresql-11.4-1-windows-x64.exe --install_runtimes 0

Be sure to select a directory other than ProgramFiles.
The installer should by default install PostgreSQL as a service and start the service.

In order to start and stop the service you will need to be running a cmd window as administrator or open the Windows Services dialog.

You can use the following cmd commands to start and stop the PostgreSQL service.
This assumes your service was named "postgresql-x64-11"
The Windows Services dialog will have the exact name of your installed service if you need to confirm this.

net start postgresql-x64-11
net stop postgresql-x64-11

In order to use the documented pg_ctl command, you will need to set the following environmental variables in your system.
The following assumes you installed PostgreSQL in **C:\PostgreSQL**

Add to System variables Path:

```
C:\PostgreSQL\bin
```
Create the following new System variables

```
PGDATA
C:\PostgreSQL\data
```

```
PGDATABASE
postgres
```

```
PGUSER
postgres
```
```
PGPORT
5432
```

```
PGLOCALEDIR
C:\PostgreSQL\share\locale
```
If your Windows PostgreSQL service is still running, you should now be able to control the server via the documented pg_ctl commands documented here

If you open a new cmd window and type pg_ctl status you should see something like

pg_ctl: server is running (PID: 9344)
C:/PostgreSQL/bin/postgres.exe "-D" "C:\PostgreSQL\data
Be aware that these commands override your windows service commands.
This means that if you stop and start the server via the pg_ctl commands it will then be running under the cmd and not the service, therefore; if you close the current cmd window it will shut down your server.

**Create a local db**

Once postgres server has started (in this case using the services.msc activate since Postgres instalation is with GUI):


**Connect to server**
```
psql -U postgres
```

Then your connected with the postgres server shell. This looks something like this:
```
postgres=# 
```

**Creating role with password (prueba 12345)**
```
CREATE user prueba with password '12345';
```

**Creating db (pruebadb)**

```
CREATE DATABASE pruebadb;
```

**Grants privileges in db (pruebadb) to role (prueba)**
```
GRANT ALL PRIVILEGES ON DATABASE pruebadb TO prueba;
```

**Log out postgre user(\q) and log in the role just created(prueba)**
```
psql -U prueba -d pruebadb -h 127.0.0.1 -W
```

### Python 3.6.8

**Install the python-3.6.8-amd64.exe file using the default instalation and add Python 3.6 to PATH**

```
Default path
C:\Users\User\AppData\Local\Programs\Python\Python36
```

```
Add Python 3.6 to PATH
```

**Verify that python is installed in the global enviroment variables by typing on cmd**

```
python --version
```

**Install pip version 9.0.3 for this project**

```
pip install pip==9.0.3
```

**Install the latest virtualenv**

```
pip install virtualenv
```

**Clone only the local branch from the repo (the local branch is the one connected to the local db, the master branch is the one running on heroku)**

```
git clone https://github.com/Yoimer/django-local-heroku.git --branch local --single-branch
```

**Get on django-local-heroku folder open cmd (or PowerShell) and create an virtual enviroment**

```
python -m venv env
```

**cd to env\Scripts folder and activate the virtual enviroment**

```
activate.bat (if using cmd)
```

```
Activate.ps1 (if using PowerShell)
```

**Install all the python packages required using pip**
```
pip install -r requirements.txt
```

## Running the tests

**In order to connect for the first time with the postgresql db or apply any change to your data, migrate**

```
python manage.py migrate 
```

**Creating a Django db super user (this has nothing to do with postgresql server)**

```
python manage.py createsuperuser
```

**Start the Django Server**

Run the Django runserver command and go to your browser and type http://127.0.0.1:8000/ 

```
python manage.py runserver
```

**Start Adding values to the db**

Type http://127.0.0.1:8000/admin on browser and enter the credentials previously set with python manage.py createsuperuser

Once values from db are populated on index file, it is time to move to production (heroku)

## Deployment

We need to create a new branch from the local branch. We'll call it master

```
git checkout master
```

We need to modify the **settings.py** file inside the **djangoair** folder

Heroku requires this adaption in order to work as expected.

Modify **DEBUG** to False and **ALLOWED_HOSTS** to all.

```python
# DEBUG = True
DEBUG = False

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['*']
```

Add **whitenoise.middleware.WhiteNoiseMiddleware** in the **MIDDLEWARE** list

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]
```
Remove the local database configuration on **DATABASES** and add the **decouple** configuration

Everytime we create a database on heroku it saves the credentials on a variable called **'DATABASE_URL'**

Using the **decouple** configuration prevents harcoding heroku crendentials on **settings.py**


```python
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'pruebadb',
#         'USER': 'prueba',
#         'PASSWORD': '12345',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

import dj_database_url
from decouple import config

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}
```

Let's add the Django **static** files configuration.

We need to create a folder called **static** inside the **root project (django-local-heroku)** folder

Since **git** does not support an empty folder, we'll create a **.keep** file inside of **static** with nothing as content

``` python
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

**Generate Procfile in root directory. It has to have the project name (in our case is djangoair)**

```
web: gunicorn djangoair.wsgi --log-file -
```

**Sign up on heroku for a new account**

https://www.heroku.com

**Download and install the **heroku cli** depending on your **OS**

https://devcenter.heroku.com/articles/heroku-cli

**Heroku is installed in the **global path** by default. Login with your account from **cmd** by typing:**

```
heroku login
```

**Create an app including its name (in our case it is djangoair)**

```
heroku create appname djangoair
```

**Add heroku git remote repository**

```
heroku git:remote -a djangoair
```

**Create postgresql db in heroku**

heroku addons:create heroku-postgresql:hobby-dev --app appname (in our case djangoair)

```
heroku addons:create heroku-postgresql:hobby-dev --app djangoair
```

**Push to heroku**

```
git push heroku master
```

Before migrating in heroku, let's push our local db.

Local db has to be already set up via cli as mentioned on readme.md

Local db has to have data already from django app in local git branch **(As explained before)**

In this case this is the first time we're going to make the db pushing

heroku pg:push localdb DATABASE_URL --app appname

```
heroku pg:push pruebadb DATABASE_URL --app djangoair
```
**Enter local db password anytime it is prompted**

## When pushing after the **first time**, heroku db has to be resetted.

heroku pg:reset --app appname --confirm appname (in our case djangoair)

```
heroku pg:reset --app djangoair --confirm djangoair
```

Enter local db password anytime it is prompted

**Migrate in heroku**

heroku run python manage.py migrate -a appname (in our case djangoair)

```
heroku run python manage.py migrate -a djangoair
```

**Create django super user on heroku**

heroku run python manage.py createsuperuser -a appname (in our case djangoair)

```
heroku run python manage.py createsuperuser -a djangoair
```