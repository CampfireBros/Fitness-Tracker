from app.database.db_connection import user_collection as usersdb
import json
from flask import Blueprint, request, render_template
from app.users.user_model import User
from app.utils.validators import MyValidator
from app.utils.msg_tools import ResponseTools as msg_tools

###########################################################################
# blueprint for flask
users = Blueprint('users', __name__, url_prefix='/users')

###########################################################################
# validation


def validate_objectid(field, value, error, db):
    if not re.match('[a-f0-9]{24}', value) and db.find_one({'_id': ObjectId(value)}):
        error(field, ERROR_BAD_TYPE.format('ObjectId'))


# validator for unique type
def validate_unique(field, value, error, db, search):
    if db.find_one({search: value}):
        error(field, "value '%s' is not unique" % value)
        
#validate_email = lambda field, value, error: validate_unique(field, value, error, usersdb, 'email')
#validate_token = lambda field, value, error: validate_unique(field, value, error, usersdb, 'token')

###########################################################################
# user schema

schema = {
    # Schema definition, based on Cerberus grammar. Check the Cerberus project
    # (https://github.com/nicolaiarocci/cerberus) for details.
    'firstname': {
        'type': 'string',
        'minlength': 1,
        'required': True
    },
    'lastname': {
        'type': 'string',
        'minlength': 1,
        'required': True
    },
    'email': {
        'type': 'string',
        'required': True
    },
    'password': {
        'type': 'string'
    },
    'token': {
        'type': 'string',
        'required': True
    },
    'tokenTTL': {
        'type': 'integer',
        'required': True
    },
    'is_auth': {
        'type': 'boolean',
        'required': True
    },
    # 'role' is a list, and can only contain values from 'allowed'.
    'roles': {
        'type': 'list',
        # admins can do anything, superusers can't edit student and faculty accounts at will
        'allowed': ['user', 'admin']
    }
}

schemaValidator = MyValidator(schema)

###########################################################################
# API Endpoints


##
# add a user to the system
# need a firstname, lastname, email, password
@users.route('/addUser', methods=['POST'])
def add_user():
    data = json.loads(request.data)
    email = data['email']
    email = User.fix_email_bug(email)

    password = User.gen_pw_hash(data['password'], data['email'])
    user = User(data['firstname'], data['lastname'], email, password)
        
    data = user.json_dump(True)
    if schemaValidator.validate(data):
        o_id = usersdb.insert_one(data).inserted_id
        user.send_verify(o_id)
        print data
        return msg_tools.response_success(objects={'user': {'user_oid': str(user.email), 'token': user.token}})
    return msg_tools.response_fail(objects=schemaValidator.errors)


##
# verifies a user from the email url
# renders a success or failure template
@users.route('/verifyUser/<o_id>/<token>', methods=['GET'])
def verify_user(o_id, token):
    if User.authorize(o_id, token):
        return render_template("successfulAuthorization.html")
    else:
        return render_template("failedAuthorization.html")


##
# get the user information from the system using an email and password or email and token
# returns the user information if request is valid
# @users.route('/getUser/id/<id>/<auth_token>', methods=['GET'])    #add later if needed
@users.route('/getUser/pw/<email>/<password>')
@users.route('/getUser/tk/<email>/<auth_token>', methods=['GET'])
def get_user(email, password = None, auth_token = None):
    user = User.get_user_if_auth(email=email, token=auth_token, password=password)
    if user is not None:
        return msg_tools.response_success(objects=user.json_dump())
    else:
        return msg_tools.response_fail(code=401, objects={'error': 'permission denied'})
