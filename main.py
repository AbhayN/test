from bottle import route, run, request
from peewee import *
import datetime as dt
import json
from playhouse.shortcuts import model_to_dict
import pprint

db = SqliteDatabase('logvba.db')


class BaseModel(Model):
    class Meta:
        database = db


class UserLog(BaseModel):
    username = CharField()
    log_datetime = DateTimeField(default=dt.datetime.utcnow())


@route('/monitor')
def index():
    accum = {}
    for ul in UserLog.select():
        accum[ul.id] = model_to_dict(ul)

    return json.dumps(accum, default=str)


@route('/log', method='POST')
def log():
    post_data = str(request.body.read())
    tokens = post_data.split("::")
    ul = UserLog(username=tokens[0], log_datetime=dt.datetime.utcnow())
    ul.save()


db.connect()
db.create_tables([UserLog])

run(host='localhost', port=8080)
