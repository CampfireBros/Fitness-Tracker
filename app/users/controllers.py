from app.database.db_connection import user_collection as usersdb
import json
import app
from flask import Blueprint, request, render_template, make_response
from app.users.user_model import User
from app.utils.validators import MyValidator
from app.utils.msg_tools import ResponseTools as msg_tools
from flask.ext.mail import Message

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
        
validate_email = lambda field, value, error: validate_unique(field, value, error, usersdb, 'email')
validate_token = lambda field, value, error: validate_unique(field, value, error, usersdb, 'token')

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
        'required': True,
        'validator': validate_email
    },
    'password': {
        'type': 'string'
    },
    'style': {
        'type': 'string',
        'required': True
    },
    'gender': {
        'type': 'string',
        'required': True
    },
    'log': {
        'type': 'dict'
    },
    'token': {
        'type': 'string',
        'required': True,
        'validator': validate_token
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
    user = User(data['firstname'], data['lastname'], email, password, data['style'], data['gender'])
        
    data = user.json_dump(True)
    if schemaValidator.validate(data):
        o_id = usersdb.insert_one(data).inserted_id
        user.send_verify(o_id)
        return msg_tools.response_success(objects=user.json_dump())
    return msg_tools.response_fail(objects=schemaValidator.errors)


##
# verifies a user from the email url
# renders a success or failure template
@users.route('/verifyUser/<o_id>/<token>', methods=['GET'])
def verify_user(o_id, token):
    if User.authorize(o_id, token):
        return make_response(open('app/templates/successfulAuthorization.html').read())
    else:
        return make_response(open('app/templates/failedAuthorization.html').read())


@users.route('/logExercise/<token>', methods=['POST'])
def log_exercise(token):
    user = User.get_user_if_auth(token=token)
    if user is not None:
        data = json.loads(request.data)
        date = data["date"]
        for exercise in data['exercises']:
            muscle = exercise['muscle']
            exer = exercise['exercise']
            if muscle in user.log:
                if exer in user.log[muscle]:
                    user.log[muscle][exer].append({'date': date, 'sets': exercise['sets'], 'notes': exercise['notes']})
                else:
                    user.log[muscle][exer] = [{'date': date, 'sets': exercise['sets'], 'notes': exercise['notes']}]
            else:
                user.log[muscle] = {}
                user.log[muscle][exer] = [{'date': date, 'sets': exercise['sets'], 'notes': exercise['notes']}]
        usersdb.update_one({"email": user.email}, {"$set": {"log": user.log}})

        msg = Message("Your exercise log",
                      sender=("ExerciseDb", app.app.config['MAIL_USERNAME']),
                      recipients=[user.email])
        msg.html = request.data
        if not app.app.config['TESTING']:
            app.mail.send(msg)
        return msg_tools.response_success()
    else:
        return msg_tools.response_fail(code=401, objects={'error': 'permission denied'})


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


@users.route('/exerciseLog/<muscle>/<exercise>/<auth_token>')
def get_log(muscle, exercise, auth_token):
    user = User.get_user_if_auth(token=auth_token)
    if user is not None:
        if muscle in user.log and exercise in user.log[muscle] and len(user.log[muscle][exercise]) > 0:
            exercise_logs = user.log[muscle][exercise]
            return msg_tools.response_success(objects=json.dumps(exercise_logs))
    return msg_tools.response_fail(code=401, objects={'error': 'permission denied'})