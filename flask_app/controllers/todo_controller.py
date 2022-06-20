from flask_app import app
from flask import session, render_template, request, redirect
from flask_app.models.todo_model import Todo
from flask_app.models.user_model import User

list_todos = []


@app.route( "/todos" )
def get_all_todos():
    if User.validate_session() == False:
        return redirect( "/login" )
    else:  
        if "num_of_visits" in session:
            session["num_of_visits"] += 1
        else:
            session["num_of_visits"] = 1

        list_todos = Todo.get_all()

        return render_template( "index.html", list_todos = list_todos )

@app.route( "/todo/new" )
def display_create_todo():
    if User.validate_session() == False:
        return redirect( "/login" )
    else:
        return render_template( "todoForm.html" )

@app.route( "/todo/new", methods = [ 'POST' ] )
def create_todo():
    Todo.create( request.form )
    return redirect( "/todos" )


@app.route( "/todo/<int:id>/update" )
def get_todo_by_id( id ):
    if User.validate_session() == False:
        return redirect( "/login" )
    else:
        data = {
            "id" : id
        }
        # call get_one in the Todo model
        current_todo = Todo.get_one( data )
        return render_template( "editTodoForm.html", current_todo = current_todo )

@app.route( "/todo/<int:id>/update", methods = [ 'POST' ] )
def update_todo_by_id( id ):
    data = {
        "id" : id,
        "status" : request.form[ 'status' ],
        "todo" : request.form[ 'todo' ]
    }
    Todo.update_one( data )
    return redirect( "/display/user" )

@app.route( "/todo/<int:id>/delete")
def delete_todo_by_id( id ):
    data = {
        "id" : id
    }
    Todo.delete_one( data )
    return redirect( "/display/user" )


    """
GET - read and display
URL of the route to display all: the name of the list or dictionary that we are about to display
Example: "/todos"
Example: "/users 

Function: get_all_todos()

URL of the route to display one: the name of the list in singular that we are about to display
followed by the id
Example: "/todo/<int:id>"
Example: "/user/<int:id>"

Function: get_todo_by_id( id )

POST - create
URL of the route to create something new: the name of the list in singular that we are about to create
followed by the keyword /new
Example: "/todo/new"
Example: "/user/new

Function: create_todo()

PUT - update
URL of the route to update something already existing: the name of the list in singular that we are about 
to update, followed by the id, followed by the keyword /update /edit
Example: "/todo/<int:id>/update"
Example: "/user/<int:id>/update"

Function: update_todo_by_id( id )

DELETE - remove
URL of the route to delete something already existing: the name of the list in singular that we are about 
to delete, followed by the id, followed by the keyword /delete /remove
Example: "/todo/<int:id>/delete"
Example: "/user/<int:id>/remove"

Function: delete_todo_by_id( id )

"""