import db
from . import app
from server.utils.utils import action_success, action_fail, check_required, get_synonyms
from flask import request,render_template,redirect,url_for
from functools import wraps

def form_require(required_args):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            missing_fields = check_required(required_args, request.form)
            if missing_fields:
                return action_fail({"missing_fields" : missing_fields}, 422,
                        message="required fields are missing")
            else:
                return f(*args, **kwargs)
        return decorated_function
    return decorator

def url_require(required_args):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            missing_fields = check_required(required_args, request.url)
            if missing_fields:
                return action_fail({"missing_fields" : missing_fields}, 422,
                        message="required fields are missing")
            else:
                return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route("/", methods = [ 'GET' ])
def home():
    return render_template('base.html')

@app.route("/<string:word>", defaults={'letter': None}, methods = [ 'GET' ])
@app.route("/<string:word>/<string:letter>", methods = [ 'GET' ])
def synonyms(word, letter):
    # TODO: add synonyms (before filter) to localdb
    syns = get_synonyms(word)
    if letter:
        syns = filter(lambda word: not letter in word, syns)
    return action_success(list(syns))
