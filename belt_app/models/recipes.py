from os import stat
from config.mysqlconnection import connectToMySQL
from belt_app import app
from flask import flash
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls, data):
        query = "SELECT * FROM recipes WHERE user_id=%(id)s"
        results = connectToMySQL('recipes').query_db(query, data)
        recipes = []
        for recipe in results:
            recipes.append( cls(recipe))
        return recipes

    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, under_30, user_id, created_at, updated_at) VALUES (%(name)s, %(description)s, %(instructions)s, %(under_30)s, %(user_id)s, NOW(), NOW())"
        saved = connectToMySQL('recipes').query_db(query, data)
        return saved

    @classmethod
    def get_recipe_by_id(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL('recipes').query_db(query, data)
        if len(results) > 0:
            return results[0]
        else:
            return False

    @classmethod
    def edit_recipe(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, created_at=%(created_at)s, under_30=%(under_30)s;"
        results = connectToMySQL('recipes').query_db(query, data)
        return results

    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id= %(id)s;"
        results = connectToMySQL('recipes').query_db(query, data)
        return results

    @staticmethod
    def validate_recipe(recipe):
        is_valid=True
        if len(recipe['name'])==0:
            flash("Name is required.", "name")
            is_valid=False
        elif len(recipe['name'])<2:
            flash('Name must be at least two characters in length', 'nam')
            is_valid = False

        if len(recipe['description'])==0:
            flash("Description is required.", "description")
            is_valid=False
        elif len(recipe['description'])<2:
            flash('Description must be at least two characters in length', 'description')
            is_valid = False

        if len(recipe['instructions'])==0:
            flash("Instructions required.", "instructions")
            is_valid=False
        elif len(recipe['instructions'])<2:
            flash('Instructions must be at least two characters in length', 'instructions')
            is_valid = False

        if len(recipe['created_at'])<0:
            flash("Date made required.", "created_at")
            is_valid = False

        if len(recipe['under_30'])<2:
            flash("Choose if recipe is under or over 30 minutes", 'under_30')
            is_valid = False
        return is_valid