<!-- Credit -->
A barebones Django app, which can easily be deployed to Heroku.

This application supports the [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) article - check it out.

<!-- Running Locally -->
To push to Heroku, you'll need to install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli), as well as [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

# install pyenv for python version management
brew update && install pyenv
# install python 3.7.0
pyenv install -v 3.7.0
# install dependencies
pip install -r requirements.txt

-> setup your local_settings.py file by mofifying sample file

# create database for the project
createdb crime_clustering_api
# generate tables
python manage.py migrate
python manage.py collectstatic

# run server locally on localhost:5000
heroku local

<!-- Deploying to Heroku -->
```sh
$ heroku create
$ git push heroku master

$ heroku run python manage.py migrate
$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)
