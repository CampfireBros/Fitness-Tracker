from flask import Blueprint, make_response
from app.database.db_connection import exercise_collection as exercisesdb
from app.utils.msg_tools import ResponseTools as msg_tools

###########################################################################
# blueprint for flask
exercises = Blueprint('exercises', __name__, url_prefix='/exercises')

###########################################################################


@exercises.route('/exercisesForMuscle/<muscle>')
def get_exercises(muscle):
    exercise = exercisesdb.find_one({'muscle': muscle})
    return msg_tools.response_success(objects=exercise['exercises'])


@exercises.route('/getMuscles')
def get_muscles():
    muscles = exercisesdb.find()
    musclelist = []
    for document in muscles:
        musclelist.append(document["muscle"])

    return msg_tools.response_success(objects=musclelist)

