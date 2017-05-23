**Setup**

virtualenv kate

cd kate

Scripts/activate

unzip the code into kate directory

pip install -r requirements.txt

gunicorn runserver:app

( if the above gunicorn doesnt work, just run  ' python runserver.py ' )

This would start the application on port 5000 and will be accessible at http://127.0.0.1:5000/


**Technology**

Python

Flask

MongoDB

Mongokit ORM to connect with Mongo

Jinja for HTML Templates

Materialize

**special access**

add query string cols=2 to view a 2 column layout. By default, the search page is a single column layout

