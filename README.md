# BrightSmileDental
A Dental Management App curated for all users:  used Django, HTML, Javascript, Bootstrap and Postgres to complete this project

## Postgres Setup 
- Follow the link below for step by step procedure to install and setup Postregres

 ( https://www.2ndquadrant.com/en/blog/pginstaller-install-postgresql/ )

-  When you entered PgAdmin and started server, create a database with any name you need or instead execute the script below

  ```` CREATE DATABASE dental_db;````
  
-  After creating the database now, we can proceed to Django setup
## Django setup steps
- Go to CMD and enter script below to download the project first

  ```` git clone https://github.com/byreddyrohithreddy/BrightSmileDental ````
- Later Download needed python packages like
  ````
  pip install django
  pip install psycopg2
   ````
- Now Go the project directory like
  ````cd dentalApp ````
- Here dentalApp is project but dental is actual Django application

  ![image](https://github.com/user-attachments/assets/bc11cdb6-68f8-4171-8ce1-aa187346c8a4)

- Inside dentalApp there is settings.py where we should configure few things like DATABASES. As shown in figure below fill details of the Postgres Db created above
![image](https://github.com/user-attachments/assets/74c1b830-27c0-401d-83af-537ef436cd8d)

- After entering database details now go to manage.py in dentalApp root folder, now execute below scripts

````
 python manage.py makemigrations dental
 python manage.py migrate
````

- After successfully making migrations now its time to start the server, execute below steps to start

```` python manage.py runserver ````

### Creating admin and user 
- using below command can create admin for the project

  ```` python manage.py createsuperuser ````

- Using admin portal can create different users for the project.

  ![image](https://github.com/user-attachments/assets/ac52fca2-0c44-41cd-b9c2-157549a330c5)

### Login page

- Using the user can Login to the dashboard of the project

  ![image](https://github.com/user-attachments/assets/24f231d0-bedc-44c8-a33f-90124aa50da3)

## Details of the project 

  

