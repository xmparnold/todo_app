from flask_app import app
from flask import session, render_template, request, redirect, flash
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt( app )

@app.route( "/" )
@app.route( "/login" )
def display_login():
    if User.validate_session() == True:
        return redirect( "/todos" )
    else:
        return render_template( "loginRegistration.html" )

@app.route( "/login", methods = [ 'POST' ] )
def user_login():
    if User.validate_login( request.form ) == False:
        return redirect( "/login" )
    else:

        result = User.get_one( request.form )
        if result == None:
            flash( "Wrong credentials", "error_login" )
            return redirect( "/login" )
        else:
            if not bcrypt.check_password_hash( result.password, request.form[ 'password' ] ):
                flash( "Wrong credentials", "error_login" )
                return redirect( "/login" )
            else:
                session[ 'first_name' ] = result.first_name
                session[ 'last_name' ] = result.last_name
                session[ 'email' ] = result.email
                session[ 'id' ] = result.id
                return redirect( "/todos" )

@app.route( "/display/user" )
def get_user_by_id():
    if User.validate_session() == False:
        return redirect( "/login" )
    else:
        # User.get_one( id )
        data = {
            "id" : session[ 'id' ]
        }
        current_user = User.get_one_with_todos( data )

        # if current_user == None:
        #     user_data = {
        #         "first_name" : session["first_name"],
        #         "last_name" : session["last_name"]
        #     }
        #     current_user = User.get_one( user_data )
        return render_template( "userInfo.html", current_user = current_user )

@app.route( "/logout", methods = [ 'POST' ] )
def user_logout():
    session.clear()
    return redirect( "/login" )

@app.route( "/user/new", methods = [ 'POST' ] )
def create_user():
    if User.validate_registration( request.form ) == False:
        return redirect( "/login" )
    else:
        if User.get_one( { "email" : request.form[ 'email' ] } ) == None:
            data = {
                "first_name" : request.form[ 'first_name' ],
                "last_name" : request.form[ 'last_name' ],
                "email" : request.form[ 'email' ],
                "password" : bcrypt.generate_password_hash( request.form[ 'password' ] )
            }
            user_id = User.create( data )
            session[ 'first_name' ] = request.form[ 'first_name' ]
            session[ 'last_name' ] = request.form[ 'last_name' ]
            session[ 'email' ] = request.form[ 'email' ]
            session[ 'id' ] = user_id
            return redirect( "/todos" )
        else:
            flash( "This email is already in use, please type a different one.", "error_register_email" )
            return redirect( "/login" )