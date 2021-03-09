# bloggernator_backend_django

### Installation process

1. Install pip and dependecies:
```bash
apt-get install python-pip
python -m pip install --upgrade pip wheel setuptools virtualenv
python3 -m pip install --upgrade pip wheel setuptools virtualenv
```

2. Create virtualenv:
```bash
python -m virtualenv venv
```

3. Activate virtual env:

* Windows:
```bash
venv\Scripts\activate
```

* Linux:
```bash
source venv/bin/activate
```

4. Install: (On venv)

* Windows:
```bash
python -m pip install -r requirements.txt
```

* Linux:
```bash
python3 -m pip install -r requirements.txt
```

4.1 Maybe you need:

* Windows:
```bash
python -m pip install --upgrade pip
```

* Linux:
```bash
python3 -m pip install --upgrade pip
```

5. Create local_setting:
* Create "local_setting.py" file in "bloggernator/settings/" using "testing_setting.py" as example.

6. Migrate: apply migrations.

* Windows:
```bash
python manage.py migrate
```

* Linux:
```bash
python3 manage.py migrate
```

7. Runserver:

* Windows:
```bash
python manage.py runserver
```

* Linux:
```bash
python3 manage.py runserver
```

8. Open URL http://127.0.0.1:8000/ on the browser.


