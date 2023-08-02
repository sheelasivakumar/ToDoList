<h1>TODO LIST APPLICATION : using Flask</h1>

 Installing necessary Dependencies 

    pip install flask
    pip install sqlite3

Importing dependencies
  
    from flask import Flask, render_template, redirect, url_for,request
    import sqlite3

Creating the Database Table
    Create a database with the help of sqlite3 using the comment 
     
      conn = sqlite3.connect("database.db")

   Create  a table with columns: task_id, title, description, status <br><br>
   <img width="113" alt="image" src="https://github.com/sheelasivakumar/ToDoList/assets/96679975/53aa1147-a35e-417c-bbcd-e65610e1e931">
   <br><br>

 Instances of an Flask application 
  
        app = Flask(__name__,static_url_path = "/static")

   where static_url_path provides the Flask application an directory where our image files are stored

Create Functions for Adding the task, updating the status of the tasks (toggling), Deleting the task<br>
Implemented a Statistic Dashbord That Shows the Count of Total no of Task, No_of_ Completed tasks, No_of_ uncompleted tasks

A demo Video



https://github.com/sheelasivakumar/ToDoList/assets/96679975/ee132b33-274e-4985-bb7a-744928e79c2d



  


