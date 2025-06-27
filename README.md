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

  
