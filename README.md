# TaskManApp
* This app is developed using **Python Flask Web Framework** and **SQL Lite Database**.
* This app has basic functionality for a user to login and create tasks for him.
* The user has the ability to register himself in the database and login himself against the email and password provided 
at the time of registration.
* Then the user can create a task for himself and keep the track of it by having a deadline associated with it also the user
can mark the task as complete or incomplete and delete the task according to his requirements.
* There are two tables one is **user** having column name as 'username', 'email', 'password', 'id', the second table is a 
**task** table having column name as 'name', 'deadline', 'complete', 'id', 'user_id'(Foreign Key with user id)
* This app also has a REST API layer where one can view all the tasks created by the users, create a task using the API 
by sending POST request methid and delete a task using DELETE request method.

# Requirements
* Install SQLite From [Here](https://www.tutorialspoint.com/sqlite/sqlite_installation.htm)
* Run the following command for installing Python, Flask and Dependencies
    ```
    pip install -r requirements.txt
    ```
* If there are errors in running the above command then please install the packages listed individually.

# Usage
* Clone the repository on your system.
* Change the directory to the cloned directory.
* Run the following command
    ```
    python databasesetup.py
    python models.py
    python server.py
    ```
* Your app should now be running on ***http://localhost:7000*** or ***http://localhost:7000/index***
* The API layer is at ***http://localhost:7000/tasks*** and For deletion at ***http://localhost:7000/task/<task id>***
