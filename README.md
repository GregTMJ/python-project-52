### Hexlet tests and linter status:
[![Actions Status](https://github.com/GregTMJ/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/GregTMJ/python-project-52/actions)
[![Python CI](https://github.com/GregTMJ/python-project-52/actions/workflows/app-check.yml/badge.svg?branch=main)](https://github.com/Gregtmj/python-project-52/actions/workflows/app-check.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/3421cbe192c76198073b/maintainability)](https://codeclimate.com/github/GregTMJ/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/3421cbe192c76198073b/test_coverage)](https://codeclimate.com/github/GregTMJ/python-project-52/test_coverage)


## Getting Started

#### Clone the current repository via command:
```git clone https://github.com/GregTMJ/python-project-52.git```

***

## Requirements
* python >= 3.8
* Poetry >= 1.14
* make >= 4

***

## Required packages
* Django  ^4.0
* Python-dotenv  ^0.21
* to avoid psycopg problems, install psycopg2-binary ^2.9.4
* Every other packages are shown inside pyproject.toml

***

#### Check your pip version with the following command:
```python -m pip --version```

#### Make sure that pip is always up-to-date. If not, use the following:
```python -m pip install --upgrade pip```

#### Next install poetry on your OS. (the link is below)
[Poetry installation](https://python-poetry.org/docs/)
##### don't forget to init poetry packages with command ```poetry init```

### We will be also working with postgreSQL, so make sure that you have installed it on your OS

*** 

## Makefile 
#### For every project should be configured a Makefile to initiate the project without requiring manual commands
#### Current project starts after typing ```make setup```
#### Inside our ```make setup``` we have 3 commands hidden: 
* ```make prepare```, which is a default .env file
* ``` make install```, which makes poetry install packages from pyproject.toml
* ```make prepare-db```, which migrates all the models inside our db
***

#### After configuration, you should use ```make serve``` to start your django-server
#### This is a task manager, where you have different users than assigns tasks for others.
***
### The project has 4 apps:
* #### status: to check the stage of task
* #### users: obviously these are the users of this site
* #### labels: something close to status but more informative
* #### tasks: where you have a subject, creator, executor, the status and labels
***
### Make sure than everything works, if you have something to add, remove or update, keep in touch "gregtmj@gmail.com"