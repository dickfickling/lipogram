from flask import jsonify,redirect
from urllib import quote
import hashlib
import random
from datetime import datetime
from requests import get
import sys
from math import radians, cos, sin, asin, sqrt
from server.utils import secrets

def random_number():
    return 4

def action_fail(payload, code, status="fail", message=None):
    jsn = {"payload" : payload,
            "status" : status}
    if message:
        jsn["error_payload"] = {"code" : code,
                "message" : message}
    response = jsonify(jsn)
    response.status_code = code
    print payload
    print message
    print code
    return response

def action_success(payload, success=True):
    response = jsonify({"success" : success, "payload" : payload})
    #print message
    return response

def check_required(required_fields, given_fields):
    missing = []
    if given_fields is None:
        return "No JSON object was passed"
    for field in required_fields:
        if not field in given_fields:
            missing.append(field)
    return missing

def xstr(s):
    if s is None:
        return ""
    return str(s)

def xcurstr(cents):
    if cents is None:
        return "0.00"
    return '{0:.02f}'.format(float(cents) / 100.0)

def to_int(fstr):
    return int(round(float(fstr)*100))

def get_synonyms(word):
    ret = set()
    for part_of_speech,results in get(secrets.BHL_BASE % word).json().items():
        ret |= set(results.get('syn', []))
        ret |= set(results.get('sim', []))
    return ret
