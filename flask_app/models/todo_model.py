from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Todo:
    def __init__( self, data ):
        self.id = data[ 'id' ]
        self.todo = data[ 'todo' ]
        self.status = data[ 'status' ]
        self.user_id = data[ 'user_id' ]
        self.created_at = data[ 'created_at' ]
        self.updated_at = data[ 'updated_at' ]

    @classmethod
    def get_all( cls ):
        query = "SELECT * FROM todos;"
        result = connectToMySQL( DATABASE ).query_db( query )
        print( result )

        list_todos = []

        for row in result:
            list_todos.append( cls( row ) )

        return list_todos

    @classmethod
    def create( cls, data ):
        query = "INSERT INTO todos(todo, status, user_id ) VALUES( %(todo)s, %(status)s, %(user_id)s );"

        id_new_todo = connectToMySQL( DATABASE ).query_db( query, data )
        print( id_new_todo )
        return id_new_todo

    @classmethod
    def get_one( cls, data ):
        query = "SELECT * FROM todos WHERE id = %(id)s;"

        result = connectToMySQL( DATABASE ).query_db( query, data )

        if len( result ) > 0:
            todo = cls( result[ 0 ] )
            return todo
        else:
            return None
    
    @classmethod
    def update_one( cls, data ):
        query = "UPDATE todos SET todo = %(todo)s, status = %(status)s WHERE id = %(id)s;"
        return connectToMySQL( DATABASE ).query_db( query, data )
    
    @classmethod
    def delete_one( cls, data ):
        query = "DELETE FROM todos WHERE id = %(id)s;"

        return connectToMySQL( DATABASE ).query_db( query, data )
