from belt_app import app
from flask import render_template, request, redirect, session
from belt_app.models.users import User
from belt_app.models.recipes import Recipe

@app.route('/recipes/<id>')
def find_recipe(id):
    data = {
        "id" : id
    }
    recipe = Recipe.get_recipe_by_id(data)
    print("********************************")
    print(recipe)
    data = {
        'id' : session['user_id']
    }
    logged_in_user = User.get_user_by_id(data)
    return render_template("one_recipe.html", recipe = recipe, user = logged_in_user)

@app.route('/recipe/new')
def new_recipe_form():
    if not 'user_id' in session:
        return redirect('/')
    return render_template('new_recipe.html')

@app.route('/recipe/submit', methods=['POST'])
def submit_recipe():
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'under_30': request.form['under_30'],
        'created_at': request.form['created_at'],
        'user_id': session['user_id']
    }
    print("***************************")
    print(data)
    if not Recipe.validate_recipe(data):
        return redirect('/recipe/new')
    Recipe.save(data)
    return redirect('/dashboard')

@app.route('/recipe/edit/<id>')
def edit_page(id):
    if not 'user_id' in session:
        return redirect('/')
    data = {
        'id' : id
    }
    recipe = Recipe.get_recipe_by_id(data)
    print("********************************")
    print(data)
    return render_template("edit_recipe.html", recipe = recipe)

@app.route('/recipes/edit/submit/<id>', methods=['POST'])
def edit_recipe():
    if not 'user_id' in session:
        return redirect('/')
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'under_30': request.form['under_30'],
        'created_at': request.form['created_at'],
        'user_id': session['user_id']
    }
    if not Recipe.validate_recipe(data):
        return redirect('/recipe/new')
    Recipe.edit_recipe(data)
    return redirect('/dashboard')

@app.route('/recipes/delete/<id>')
def delete_recipe(id):
    data = {
        "id" : id
    }
    Recipe.delete_recipe(data)
    return redirect('/dashboard')