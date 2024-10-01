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

- After successful Login we get into Dashboard page


 ![image](https://github.com/user-attachments/assets/0397e0e1-8870-45c3-b832-4ea1f8c73a7f)


## Details of the project 

- This Management App have three tabs Clinics, Doctors and Patients respectively. Clicking on each will go into respective Management Apps
- The functionalities of each App are designed and implemented as per the requirements mentioned on each page.
- Implemented all procedures with robustness and Quality.
- Also wrote testcases for few implementations for future scope
- Also there are Four API endpoints to add_clinic, add_patient, add_doctor, clinic_list to post and fetch info.

## Clinic Page overview:
- Shows all clinics present and with ability to add clinic without any affiliation

![image](https://github.com/user-attachments/assets/f8301d5f-6305-4d74-bc16-f4a0fb662245)

- When clicked on clinic will show detailed view of the clinic with ability to edit info and also to add new doctors to clinic

edit clinic info 
![image](https://github.com/user-attachments/assets/a6267515-631e-48e3-ab30-b9a8c0277fa6)

edit doctor info and add_doctor button
![image](https://github.com/user-attachments/assets/cafcb94c-1c95-4957-b5ca-02fc9561e5c9)

add doctor by entering info
![image](https://github.com/user-attachments/assets/1389623e-84b2-4111-a058-8962000be360)

- These functionalities work, and you can test them actually
## Doctor Page Overview:
- Shows all the doctors with the number of clinics and patients they are associated, we can also add doctor without any affiliation to clinic here
![image](https://github.com/user-attachments/assets/0a609eb8-1f25-4d4a-96ba-23c6edc33abc)

- Add doctor without any affiliation
![image](https://github.com/user-attachments/assets/07d383d5-b773-4be6-9977-444d88f01c9e)

- When clicked on each Doctor will show a details and ability to edit the doctor details
![image](https://github.com/user-attachments/assets/b81942b0-5930-4f4a-81ec-ec63da4b1d87)

- We can see all patients associated with the doctor.

## Patient Page Overview:
- This is main functionality of this entire Application, below is the main page which shows all patient details and ability to add patient without any affiliation to the patients list.

![image](https://github.com/user-attachments/assets/80628f1e-b9c1-4a5e-b0e0-3e87d6a9599c)

Add patient here
![image](https://github.com/user-attachments/assets/a57aea8d-c526-4094-b3e9-9a8dd7d6bb0e)

- When I click on the patient, it will show details of the patient with the ability to edit them,  Which will show previous visits and next appointment details.  

![image](https://github.com/user-attachments/assets/732e35bb-06d3-45b5-a7a9-6712e43e15bc)

- On the bottom of the page we have schedule_appointment, when clicked on appointment will show a page where we have to choose details sequentially to book an appointment.
  -  First select procedure, will show relevant clinics with the procedure
  -  select clinic from available list, on selection will show doctors who has specialization in the procedure
  -  choose a doctor, upon selection will show a calendar to choose a date
  -  When choosed a Date, will show available slots on the particular day considering schedule of the Doctor and also time slots booked before by other patients.

- The below picture depicts the functionality of details to schedule an appointment.
  ![image](https://github.com/user-attachments/assets/f7fb5adc-8fe7-4f57-919b-0d384b783624)

## Executing Testcases wrote:
- Wrote 6 test cases for testing few basic functionalities like add_clinic, add_patient, add_doctor
- Can execute testcases by running command ```` python manage.py test dental ````

## Challenges faced:
- This is a big project with a lot of dependencies and functions, so designing and making the outline itself is a challenging task.
- Programming for HTML is difficult as it has a lot of values and functions that need to be included, we reused a lot of functions in HTML to decrease complexity.
- Admin and user access are difficult to implement for each particular user, so we will implement those features in the future.
- The main files are models.py, views.py, and all templates. These files constitute 90% of the code so making changes and updating them is difficult
- Keeping flow and URLs is difficult as they have a lot of functions that overlap.
- The ability to think and design myself without properly mentioning details in the project description or ambiguous details is challenging a little bit.

## Future scope:
- Can integrate an AIBot for managing all services without the user explicitly working. This bot can add clinics, patients, doctors, can even fetch details and finally can schedule appointments.
- Access based on the user, where hiding few details from other users.  

## References:
- https://realpython.com/django-setup/#install-django-and-pin-your-dependencies
- https://stackpython.medium.com/how-to-start-django-project-with-a-database-postgresql-aaa1d74659d8
- https://www.postgresql.org/download/
- https://medium.com/@satyarepala/a-comprehensive-guide-to-django-views-understanding-types-and-use-cases-4a02a078ced
- https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Models
- https://www.w3schools.com/bootstrap/
- https://forum.djangoproject.com/t/loading-views-with-javascript/14001
 



