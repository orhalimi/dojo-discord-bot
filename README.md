# Discord Bot

Discord Bot is a web application for dealing with discord bot mentoring classes.


# Configure
```bash
# Create a virtual environment

python3 virtualenv env

# Activate the environment

source env/bin/activate
```
# Installation
install requirements using package manager [pip](https://pip.pypa.io/en/stable/)
```
pip install -r requirements.txt

# create an development sqlite3 database
(env) python3 manage.py makemigrations webapp
(env) python3 manage.py migrate

# creating the three roles
(env) python3 setup.py

# start the server
(env) python3 manage.py runserver

# create admin account to use the ORM features
(env) python3 manage.py createsuperuser

# open "http://localhost:8000/admin" to connect 
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)