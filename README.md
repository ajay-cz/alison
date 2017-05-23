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


**Overview**

This is a sample Web Application created with Python Flask with MongoDB as the Backend.
The json dataset was Imported to the MongoDB.
This project is about creating a web application with Python using Flask framework & MongoDB. To demonstrate the searching and filtering capability of a large data sets with the help of python and mongo DB. We use materialize for the UI designs.

Basic application contains two main pages 1 ) The homepage and 2) The search page.

The Search page has been designed with a two column layout : the the left column contains the filters and the right column contains the data listing. For the filters we have a simple form with various filter keys. As the user tries to select any of the filter options, a request is sent to the flask application, which would then process the parameters and fire a query to the mongo DB, with the respective arguments.

Once we get the result set from mango we process this to determine the filters and the values for each of these filters which are then rendered back to the HTML template and respective default values are set on to the HTML templates