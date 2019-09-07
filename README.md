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


### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
