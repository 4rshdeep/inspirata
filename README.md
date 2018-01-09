# Code.fun.do
## Quickstart ##

Make sure you have [pipenv installed](https://docs.pipenv.org/install.html). Then install Django 2.0 in your virtualenv:

    pip install django==2.0


cd to your project(cd inspirata/) and install the development dependences

    pipenv install --dev

If you need a database, edit the settings and create one with
   
    pipenv run python manage.py migrate

Once everything it's setup you can run the development server: [http://localhost:8000/](http://localhost:8000/)

    pipenv run python manage.py runserver
