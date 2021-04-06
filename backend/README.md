# bloggernator_backend_django

### Installation process

Depending on the system the command can vary 'python' or 'python3'


#### 1. Install pip and dependecies:
```bash
apt-get install python-pip

python -m pip install --upgrade pip wheel setuptools virtualenv
```

#### 2. Create virtualenv:
```bash
python -m virtualenv venv
```

#### 3. Activate virtual env:

* Windows:
```bash
venv\Scripts\activate
```

* Linux:
```bash
source venv/bin/activate
```

#### 4. Install: (On venv)
```bash
python -m pip install -r requirements.txt
```

* Maybe you need:
    ```bash
    python -m pip install --upgrade pip
    ```

#### 5. Create local_setting:
Create "local_setting.py" file in "bloggernator/settings/" using "testing_setting.py" as example.

#### 6. Testing:
Test that everything works correctly
```bash
python manage.py test --settings=bloggernator.settings.testing_settings
```

#### 7. Migrate:
Apply migrations.

```bash
python manage.py migrate
```

#### 8. Runserver:
```bash
python manage.py runserver
```

