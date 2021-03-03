# bloggernator_backend_django

### Installation process

1. Install pip and dependecies:
    $ apt-get install python-pip
    $ python -m pip install --upgrade pip wheel setuptools virtualenv
    $ python3 -m pip install --upgrade pip wheel setuptools virtualenv

2. Create virtualenv:
    $ python -m virtualenv venv

3. Activate virtual env:
    Windows:
        $ venv\Scripts\activate
    Linux:
        $ source venv/bin/activate

4. Install: (On venv)
    Windows:
        $ python -m pip install -r requirements.txt
    Linux:
        $ python3 -m pip install -r requirements.txt

    Maybe you need:
        Windows:
            $ python -m pip install --upgrade pip
        Linux:
            $ python3 -m pip install --upgrade pip

5. Create local_setting:
    Create "local_setting.py" file in "bloggernator/settings/" using "testing_setting.py" as example.

6. Migrate: apply migrations.
    Windows:
        $ python manage.py migrate
    Linux:
        $ python3 manage.py migrate

7. Runserver:
    Windows:
        $ python manage.py runserver
    Linux:
        $ python3 manage.py runserver

8. Open URL http://127.0.0.1:8000/ on the browser.


