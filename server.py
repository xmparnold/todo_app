from flask import Flask
from flask_app import app
from flask_app.controllers import todo_controller, user_controller




if __name__ == "__main__":
    app.run(debug = True)

