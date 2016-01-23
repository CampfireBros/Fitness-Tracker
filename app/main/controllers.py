from flask import Blueprint, make_response

###########################################################################
# blueprint for flask
main = Blueprint('main', __name__)

###########################################################################


@main.route('/')
@main.route('/signin')
@main.route('/signup')
def basic_pages():
    return make_response(open('app/templates/index.html').read())


