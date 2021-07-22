from config.mysqlconnection import connectToMySQL
from belt_app import app
from flask import flash
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

LETTERS_ONLY_REGEX = re.compile(r'^[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL('recipes').query_db(query)
        users = []
        for user in results:
            users.append( cls(user))
        return users

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL('recipes').query_db(query, data)

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users where id=%(id)s;"
        results = connectToMySQL('recipes').query_db(query, data)
        if len(results) < 0:
            return False
        return cls(results[0])

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users where email=%(email)s;"
        results = connectToMySQL('recipes').query_db(query, data)
        if results == 0:
            return False
        return cls(results[0])

    @classmethod
    def email_not_in_db(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('recipes').query_db(query, data)
        return len(results) == 0

    @staticmethod
    def validate_registration(user):
        is_valid = True
        if len(user['first_name'])==0:
            flash("First Name is required.", "first_name")
            is_valid=False
        elif len(user['first_name'])<2:
            flash('First Name must be at least two characters in length', 'first_name')
            is_valid = False
        elif not LETTERS_ONLY_REGEX.match(user['first_name']):
            flash("First name must not contain non-alphabetic characters", 'first_name')
            is_valid=False

        if len(user['last_name'])==0:
            flash("Last Name is required.", "last_name")
            is_valid=False
        elif len(user['last_name'])<2:
            flash('Last Name must be at least two characters in length', 'last_name')
            is_valid = False
        elif not LETTERS_ONLY_REGEX.match(user['last_name']):
            flash("Last name must not contain non-alphabetic characters", 'Last_name')
            is_valid=False

        if len(user['email']) == 0:
            flash("Email is required", 'email')
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']):
            flash("Invalid email format. Must meet ", 'email')
            is_valid=False
        elif not User.email_not_in_db(user):
            flash('A user with that email already exists', 'email')
            is_valid = False
        
        if len(user['password'])==0:
            flash("Password is required.", "password")
            is_valid=False
        elif len(user['password']) < 8:
            flash('Password must be at least 8 characters.', 'password')
            is_valid = False
        elif user['password'] != user['con_password']:
            flash("Password must match confirm password.", 'password')
            is_valid = False
        return is_valid


    @staticmethod
    def validate_login(login_user):
        is_valid = True
        user_not_in_db = User.email_not_in_db(login_user)
        if user_not_in_db:
            flash('Invalid email/password.', "login_email")
            is_valid = False
        return is_valid