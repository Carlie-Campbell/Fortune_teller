# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re
ALPHA = re.compile(r"^[a-zA-Z]+$")
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$")

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# ----------------Create a user--------------
    @classmethod
    def create(cls, data):
        query = """
        INSERT INTO users (first_name,last_name,email,password)
        VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);
        """
        return connectToMySQL(DATABASE).query_db(query,data)
    
    # ----------Get user by id-----------
    @classmethod
    def get_by_id(cls, data):
        query  = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False
    

    # --------For validation/login/making sure email isn't already in use-----------
    @classmethod
    def get_by_email(cls, data):
        query  = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False
    
    # --------------Validator for login----------
    @staticmethod
    def validator(data):
        print('data',data)
        is_valid = True
        if len(data['first_name']) < 1:
            is_valid = False
            flash('First name required', 'reg')
        elif len(data['first_name']) < 2:
            is_valid = False
            flash('First name must be 2 characters', 'reg')
        elif not ALPHA.match(data['first_name']):
            is_valid = False
            flash('First name must be letters only', 'reg')
        if len(data['last_name']) < 1:
            is_valid = False
            flash('Last name required', 'reg')
        elif len(data['last_name']) < 2:
            is_valid = False
            flash('Last name must be 2 characters', 'reg')
        elif not ALPHA.match(data['last_name']):
            is_valid = False
            flash('Last name must be letters only', 'reg')
        if len(data['email']) < 1:
            is_valid = False
            flash('Email required', 'reg')
        elif not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash('Email must be valid format','reg', 'reg')
        else:
            potential_user = User.get_by_email({'email': data['email']})
            if potential_user:
                flash('email already exists, please try again', 'reg')
                is_valid = False
        if len(data['password']) < 1:
            flash('Password required' 'reg')
            is_valid = False
        elif len(data['password']) < 8:
            flash('Passsword must be at least 8 characters', 'reg')
            is_valid = False
        elif data['password'] != data['confirm_pass']:
            flash('Passwords must match', 'reg')
            is_valid = False
        return is_valid