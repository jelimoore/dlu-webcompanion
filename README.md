# DLU-WebCompanion
A better DarkFlame Universe web companion app.

## Features
User Features:
- Displays leaderboards from in-game
- Request name change [WIP]
- Password reset via email [WIP]
- Play key activation

Admin Features:
- Player and Pet name approval
- Property name approval
- Kick/ban in-game via web interface (no need to log into LU)

## Setup

First, create a virtualenv with venv:
```
python3.9 -m venv .
source bin/activate
```

Then, install the requirements:
```
pip install -r requirements.txt
```

Next, set up your config file. Start by copying the `config.sample.py` file to `config.py`. Then, you will need to set your database info and generate a secret key. Do this with `os.urandom(12).hex()`. The databse should be the exact same DB that DLU runs on. This app does not need a separate database.

You will need to set these two options, at minimum:

```
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://user:pass@host/dbname"
SECRET_KEY = "[key from urandom generation]"
```

For example, if your username is `dlu_user`, pass is `dlu_pass`, database server is `localhost`, and the database name is `dlu`, your connection string would look like this:
```
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://dlu_user:dlu_pass@localhost/dlu"
```

Then, start it with
```
python app.py
```
And you're off!

Remember to use a real WSGI server such as Apache, Gunicorn, uWSGI, or others when deploying to production.

## License
This program is licensed under the GNU AGPLv3 license.