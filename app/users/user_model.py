import uuid, hashlib, binascii, base64, app
from app.database.db_connection import user_collection
from bson import ObjectId
from flask.ext.mail import Message


# user class for all users in the system
class User:
   
    DEFAULT_TTL = 500

    # constructor to create a user
    def __init__(self, firstname, lastname, email, 
                 password, style, gender, log={}, token=None,
                 is_auth=False,
                 roles=[], o_id=None):
        self.o_id = o_id
        self.f_name = firstname 
        self.l_name = lastname
        self.email = email
        self.password = password
        self.style = style
        self.gender = gender
        self.log = log
        if token is None:
            token = User.gen_token()
        else:
            token = token
        self.token = token
        self.is_auth = is_auth
        if len(roles) == 0:
            self.roles = User.get_role(email)
        else:
            self.roles = roles

    # creates a JSON dump of the
    def json_dump(self, inc_pass=False):
        if inc_pass:
            pwd = self.password
        else:
            pwd = ''
        json_dict = {
            'firstname': self.f_name,
            'lastname': self.l_name,
            'email': self.email,
            'password': pwd,
            'log': self.log,
            'token': self.token,
            'is_auth': self.is_auth,
            'roles': self.roles,
            'style': self.style,
            'gender': self.gender
        }
        return json_dict

    # returns if a user has a certain role
    def can_access(self, email):
        return 'admin' in self.roles or ('user' in User.get_role(email))

    # returns if a user is authorized (verified email)
    def is_authorized(self):
        return self.is_auth

    # send the verification email to the user
    def send_verify(self, o_id):
        hash_token = User.gen_token_hash(self.token)
        html_body = "Please verify your account by clicking the link below!<br>"
        msg_body = "<a href='http://{0}:{1}/users/verifyUser/{2}/{3}'>Click Here!</a><br><br>".format(app.app.config['HOST'],
                                                                   app.app.config['PORT'],
                                                                   o_id, hash_token)
        rest = "If the link above does not work, copy and paste the following link into your browser:<br>"\
            "http://{0}:{1}/users/verifyUser/{2}/{3}'".format(app.app.config['HOST'],
                                                                   app.app.config['PORT'],
                                                                   o_id, hash_token)
        msg = Message("Verfy with ExerciseDB",
                      sender=("ExerciseDb", app.app.config['MAIL_USERNAME']),
                      recipients=[self.email])
        msg.html = html_body + msg_body + rest
        if not app.app.config['TESTING']:
            app.mail.send(msg)


    # generates a unique token
    @staticmethod
    def gen_token():
        return str(uuid.uuid1())

    # generates a password hash
    @staticmethod
    def gen_pw_hash(password, sugar):
        # TODO make salt more unique
        salt = app.app.config['SALT'] + sugar
        return hashlib.sha512(password + salt).hexdigest()

    # generates a token hash
    @staticmethod
    def gen_token_hash(token):
        # creates a url safe hash token
        return base64.urlsafe_b64encode(hashlib.md5(token).digest())[:11]

    # authorizes a user - triggered from verification email
    @staticmethod
    def authorize(o_id, token):
        tmp_user = User.get_user_from_db(o_id = o_id)
        tmp_user_token = User.gen_token_hash(tmp_user.token)
        if tmp_user_token == token:
            user_collection.result = user_collection.update_one(
                {'_id': ObjectId(o_id)},
                {
                    '$set': {'is_auth': True}  # increase as nesseceary
                })
            return True
        else:
            return False

    # returns roles based on the email address
    @staticmethod
    def get_role(email):
        # TODO use full email
        if 'soccer62394' in email or 'jtassone93' in email:
            return ['admin', 'user']
        else:
            return ['user']
        
    # fixes the exploit that allows users to repeatedly register with the same email account
    @staticmethod
    def fix_email_bug(email):
        if '+' in email:
            l = email.split('+')
            l2 = l[1].split('@')
            if len(l2) > 1:
                return l[0] + '@' + l2[1]
            else:
                return l[0] + l[1]
        else:
            return email

    # gets a user from the database based on one of the input fields
    @staticmethod
    def get_user_from_db(o_id=None, token=None, email=None):
        if token is not None:
            mongo_user = user_collection.find_one({'token': token})
        elif o_id is not None:
            mongo_user = user_collection.find_one({'_id': ObjectId(o_id)})
        else:
            mongo_user = user_collection.find_one({'email': email})
            
        if mongo_user is None:
            return None
        user = User(mongo_user['firstname'],
                    mongo_user['lastname'],
                    mongo_user['email'],
                    mongo_user['password'],
                    mongo_user['style'],
                    mongo_user['gender'],
                    mongo_user['log'],
                    mongo_user['token'],
                    mongo_user['is_auth'],
                    mongo_user['roles'],
                    mongo_user['_id'])
        return user

    # returns a user if they are authorized for the role
    @staticmethod
    def get_user_check_auth(role, token, is_post=False):
        user = User.get_user_from_db(token=token)
        if user is not None:
            if role in user.roles:
                return user
        return None
    
    # returns a user if they are authorized to get that user
    @staticmethod
    def get_user_if_auth(o_id=None, token=None, email=None, password=None):
        user = User.get_user_from_db(o_id, token, email)
        if user is not None:
            if token is not None:
                if email != user.email:
                    if user.can_access(email):
                        return user
                else:
                    return user
            else:
                if user.password == User.gen_pw_hash(password, user.email):
                    return user
        return None
