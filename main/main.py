from flask import Blueprint

main = Blueprint('main', __name__)




@main.route('/register')
def register():
    return "Hello from the main blueprint"