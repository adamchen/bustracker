bustracker
==========

Bus timetable for Bath City Centre

# Setting up dev environment
(Instructions for Ubuntu 12.10)

Clone the project.
    git clone https://github.com/adamchen/bustracker

Install pip to manage packages.
    (sudo) apt-get install pip

## virtualenv
Use pip to install virtualenv and virtualnenvwrapper.
    (sudo) pip install virtualenv virtualenvwrapper

Create a virtual environment.
    mkvirtualenv bustracker

When you create a new environment it automatically becomes the active environment. Otherwise to activate an environment use the workon command.
    workon bustracker

## Install python packages
Make sure your in the top directory of the git project. Use pip to install packages in requirements.txt.
    pip install -r requirements.txt

## Install sqlite
Database used is sqlite3, the django default. Plan to move to mysql?

    (sudo) apt-get install sqlite

## Using South to load data

    ./manage.py syncdb
    ./manage.py migrate

## Running the server

    ./manage.py runserver

Open http://127.0.0.1:8000 in a browser.
Profit.
