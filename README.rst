django directory template
=========================

Description
-----------
This is my way to start a django project. It includes custom commands,
file structure skeleton and AbstractUser model for modification in django
user model.


Usage
------------

.. code-block:: bash

    # Create a root directory
    $ mkdir project && cd project/

    # Make sure we have an up-to-date version of django 2.2
    $ django-admin startproject --template=https://github.com/datasteer/hrms/archive/master.zip [project_name]

    # Install dependencies django-debug-toolbar, python-decouple
    $ pip3 install -r requirements.txt

    # One shot makemigrations and migrate
    $ python manage.py setup


Structure
---------
This project has the following directory structure::

    project_name/
    ├── app/
    │   ├── core/       # custom commands ex: py manage.py generatekey, setup
    │   └── users/      # overridden django user model
    │
    ├── config/         # includes a bunch of settings, url and wsgi
    │   ├── settings/
    │   │    ├── base,py             # inherited by development or production.py
    │   │    ├── development.py      # uses django debug toolbar
    │   │    ├── production.py       # production settings, debug = False
    │   │    ├── settings-default.py # default settings file created by django.admin
    │   │    ├── .env-example        # an example how should be the .env file
    │   │    └── .env                # in .gitignore, automatically will created
    │   │
    │   ├── urls.py
    │   └── wsgi.py
    │
    ├── locale/     # locale path for internationalization
    ├── static/     # static folder
    │   ├── css/
    │   ├── img/
    │   └── js/
    │
    ├── templates/  # templates folder
    └── manage.py

Quickstart
==========
.. code-block:: bash

    # Create a root directory
    $ mkdir project && cd project/

    # Make sure we have an up-to-date version of django 2.2
    $ django-admin startproject --template=blabla.zip [project_name]

    # Install dependencies django-debug-toolbar, python-decouple
    $ pip3 install -r requirements.txt

    # One shot makemigrations and migrate
    $ python manage.py setup

    # Overriden startapp command creates app in app directory
    # Do not worry about the folder location
    $ python manage.py startapp blog

    # Generate secret key in .env file
    $ python manage.py generatekey

Apps
====
This template is consist of users app and core app

users
-----
If you’re starting a new project, it’s highly recommended to set up a custom user model,
even if the default User model is sufficient for you. This model behaves identically
to the default user model, but you’ll be able to customize it in the future if the need arises.
https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project

core
----
Has only custom management commands. Can also be used as some
base models. Like; timestamped model.


Commands
========
Lives in core app.

setup
------
Calls:
codeblocks:: bash
    $ python manage.py makemigrations
    $ python manage.py migrate
    $ python manage.py generatekey
in order.

generatekey
------------
Creates a secret key and stores in .env file.

startapp(override)
-------------------
Starts app in app directory. Do not worry about the folder location

Todos
=====

config/settings/production.py
---------------------------------
TODO: enter site domain name only ex: ALLOWED_HOSTS['example.com']

config/settings/base.py
------------------------
TODO: change it which database you will use, at the bottom postgresql example shown

config/wsgi.py
---------------
TODO: change to production when deploy ex: 'config.settings.production'

manage.py
--------------
TODO: change to production when deploy ex: 'config.settings.production'
