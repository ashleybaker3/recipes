from belt_app import app
from belt_app.controllers import users, recipes

if __name__ == "__main__":
    app.run(debug=True)