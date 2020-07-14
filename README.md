# MyHao
A platform that allows you to start your journey towards home ownership.
Fulfil your dreams by letting us help you achieve your home ownership goals which is developed using Python/Django and PostgreSQL.

## Getting started

### Prerequisites

In order to install and run this project locally, you would need to have the following installed on you local machine.

* [**Python 3+**](https://www.python.org/downloads/release/python-368/)
* [**Django 3+**](https://www.djangoproject.com/download/) 
* [**PostgreSQL**]()


### Installation

* Clone this repository
* Navigate to the project directory `cd myhao/`
* Create a virtual environment
* Install dependencies `pip install -r requirements.txt`

* Edit `myhao/myhao_main/local_settings.py` database credentials to your database instance

* Create a PostgreSQl database 

* Run the command `python manage.py makemigrations` 

* Run the command `python manage.py migrate` to create and sync the postgreSQL database (you must have the database previously created with name 'myhao_db').

* It's needed that you have your own super user to admin the application, so run the command `python manage.py createsuperuser` and follow the instructions.

* Run the command `python manage.py runserver`

* Run development server

`python manage.py runserver`		

## Request and Response Object API guide for all Endpoints

# Testing API endpoints
<pre>
<table>
<tr><th>Test</th>
<th>API-endpoint</th>
<th>HTTP-Verbs</th>
</tr>
<tr>
<td>SignUp a user</td>
<td>/api/v1/users</td>
<td>POST</td>
</tr>
<tr>
<td>SignIn a user</td>
<td>/api/v1/users/login</td>
<td>POST</td>
</tr>
<tr>
<td>Post a profile</td>
<td>/api/v1/profile</td>
<td>POST</td>
</tr>
<tr>
<td>Edit profile</td>
<td>/api/v1/profile/id</td>
<td>PUT</td>
</tr>
<tr>
<td>Fetch a single profile</td>
<td>/api/v1/profiles/id</td>
<td>GET</td>
</tr>
<tr>
<td>Delete a profile</td>
<td>/api/v1/profile/id</td>
<td>DELETE</td>
</tr>
<tr>
<td>Post a Home</td>
<td>/api/v1/homes</td>
<td>POST</td>
</tr>
<tr>
<td>Get a single home</td>
<td>/api/v1/homes/id</td>
<td>GET</td>
</tr>
<tr>
<td>Edit a home</td>
<td>/api/v1/homes/id</td>
<td>PUT</td>
</tr>
<tr>
<td>Delete a home</td>
<td>/api/v1/homes/id</td>
<td>DELETE</td>
</tr>
<tr>
<td>Book a home</td>
<td>/api/v1/book</td>
<td>POST</td>
</tr>
<tr>
<td>Get a single home</td>
<td>/api/v1/books/id</td>
<td>GET</td>
</tr>
<tr>
<td>Fetch available books</td>
<td>/api/v1/books</td>
<td>GET</td>
</tr>
<tr>
<td>Edit a book</td>
<td>/api/v1/books/id</td>
<td>PUT</td>
</tr>
<tr>
<td>Delete a book</td>
<td>/api/v1/books/id</td>
<td>DELETE</td>
</tr>
</tr>
</table>
</pre>
* Check [here](https://docs.google.com/document/d/1J12z1vPo8S5VEmcHGNejjJBOcqmPrr6RSQNdL58qJyE/edit?usp=sharing)
* Visit `http://127.0.0.1:80/docs/

## Using Docker 
Build image

`docker build -t myhao_app .` 


