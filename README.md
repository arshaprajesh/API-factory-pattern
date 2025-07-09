About this project :

<img width="1335" alt="image" src="https://github.com/user-attachments/assets/61062899-e0d7-41a4-947c-98324ab93e94" />


Application factory pattern 

What: 

Instantiate the objects but subclass will decide which class to instantiate 

Why: 

1-Loosely couple 

2-Avoid duplication 

 
How: 

-create_app() 

-extensions.py 

-blueprints 

-models 

-app.py 

-config.py 

 

Structure  

 

/project 
├── /application 
│ ├── __init__.py - create_app() lives here 
│ ├── extensions.py 
│ ├── /blueprints 
│ │ ├──/user 
│ │ ├──__init__.py - Initialize User Blueprint 
│ │ ├── routes.py - Create User Controllers/routes 
│ │ └── userSchemas.py 
│ └── models.py 
├── app.py 
└── config.py 

 

->create a folder app(create files inside app folder) 

__init__.py 

extensions.py 

 Models.py 

 

->create file config.py 

->folder blueprint(inside the app folder) 

->folder customers(inside the blueprint folder)(create files inside customer folder) 

__init__.py 

Routes.py 

Schemas.py 

 

=================================================== 

Flask limiter 


What: 

It is an extension help to restricts the number of requests an application can receive within a given time period. 


Why: 

-protective routes from excessive traffic 


 Flask caching 

What: 

used to improve application performance by temporarily storing results and  reuse them if needed later 

Why: 

1-Caching API responses to reduce database queries 

2-Improving response times for high-traffic endpoints 

3-faster retrieval 


Lambda function

What: 

Lambda functions in Python are small functions defined with the lambda keyword 


Why: 

Lambda functions allow you to write simple functions in a single line 

 

Query parameter 

What: 

Query parameters are key-value pairs appended to the end of a URL after the ? Symbol. 

Why: 

For filtering the query without having to send a full JSON payload. 


What: 

Pagination divides large sets of data into manageable pages 

 

Why: 

delivering results in smaller 

more digestible portions 

reduces server load. 

 

Pagination methods 

1-limit 

2-offset or page 

Using limit 
https://api.example.com/products?limit=10&offset=20 

This returns 10 products, starting from the 21st product (offset 20). 

Using page 
https://api.example.com/products?page=2&page_size=10 

This fetches the second page with 10 results per page. 


syntax = http://127.0.0.1:5000/mechanics/search?name=ma


 
Run in local ,you need to install 
 
-> python3 -m venv venv 
-> source venv/bin/activate 
-> pip3 install flask flask-sqlalchemy mysql-connector-python 
->->pip install flask-marshmallow marshmallow-sqlalchemy 
->pip install Flask-Limiter
->pip install Flask-Caching 
->pip install PyJWT 
-> install postman 
->pip install Flask-Limiter
->pip install Flask-Caching 
->pip install PyJWT   

  start the project :
->run app.py
 


Test : 
Test the operations in postman

swagger
What: 
 It helps you create, maintain, and organize your API documentation in a structured and user-friendly way 


Why: 
Swagger UI provides a web-based interface where developers can view your API's endpoints, test them out, and see example requests and responses. This makes it easy for developers to understand how to use your API and integrate it into their own projects. 

How: 
pip install flask-swagger flask_swagger_ui 
Create static (folder)->swagger.yaml(file) 

Path: 

Endpoint 
Type of request (post, get, put, delete) 
tag (category for the route) 
summary 
description 
security: Points to the security definition (Only need this for token authenticated routes) 
parameters: Information about what the data the route requires(Only required for POST and PUT request) 
responses: Information about what the data  route returns (Should include examples) 
Definition(s): 

PayloadDefinition: Defines the "Shape" of the incoming data (Only required for POST and PUT requests) 
ResponseDefinitions: Defines the "Shape" of the outgoing data  


for run in swagger(using token):-
 ->click Authorize lock
->type  Bearer+token

for run:-
#in terminal 
python -m unittest discover tests 


TDD(Test Driven Development) 

What: 
TDD is a software development process where you write tests before writing the actual code 

Why: 
  improve code quality 

  speed up development 

  reduce bugs 

How: 

Import unittest  

-python3 -m venv venv 

-source venv/bin/activate 

-pip install flask 


How to open swagger: 

-Run in app.py 
-The API is running on your localhost 127.0.0.1:5000 
-Then endpoint that renders your documentation is /api/docs  

 

TDD follows a simple cycle: Red-Green-Refactor.

1-Red Phase: 

What: 
Writing a failing test 

2-Green Phase: 

What: 
Writing a simplest code to making the test pass 

3-Refactoring Phase:  

What: 
Improving the code 

for run:-
source venv/bin/activate 
run all the test files:-python -m unittest discover tests 

run all the specific test files:-python -m unittest tests.test_customer 
