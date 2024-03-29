# Discord Bot

Dojo bot is a discord bot meant to help manage both the web application and the server side activities for the Dojo programmer mentoring program. 


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


# start the server
(env) python3 manage.py runserver

# create admin account to use the ORM features
(env) python3 manage.py createsuperuser

# open "127.0.0.1:3000/admin" to connect 
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
