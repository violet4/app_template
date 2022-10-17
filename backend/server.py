#!/usr/bin/env python3
from fastapi import FastAPI, Request
from fastapi.middleware.wsgi import WSGIMiddleware
import falcon
import sqlalchemy

from models import engine, User, Base

Base.set_sess(sqlalchemy.orm.sessionmaker(bind=engine))

app = FastAPI()

# base = '/api'
base = ''


@app.get(base + '/')
def read_root():
    return {'text': 'fastapi'}


def extract(d, keys):
    return {k: getattr(d, k) for k in keys}


@app.get(base + '/user')
def get_user() -> dict:
    users = None
    with Base.get_session() as sess:
        users = sess.query(User).all()
        users = [extract(d, ['user_id', 'username']) for d in users]
    return users


@app.put(base + '/user')
def get_user(data: dict):
    username = data['username']
    user = None
    with Base.get_session() as sess:
        user = sess.query(User).where(User.username==username).one_or_none()
        if not user:
            user = User()
            user.username = username
            sess.add(user)
            sess.commit()
        return {
            'user_id': user.user_id,
            'username': user.username,
        }


@app.delete(base + '/user')
def delete_user(data: dict):
    user_id = data['user_id']
    user = None
    with Base.get_session() as sess:
        query = sess.query(User).where(User.user_id==user_id)
        user = query.one_or_none()
        if user:
            user = {
                'user_id': user.user_id,
                'username': user.username,
            }
            query.delete()
            return user


class QuoteResource:
    def on_get(self, req, resp):
        quote = {
            'quote': (
                "I've always been more interested in "
                "the future than in the past."
            ),
            'author': 'Grace Hopper'
        }

        resp.media = quote


falcon_app = falcon.App()
falcon_app.add_route('/quote', QuoteResource())

# mount
app.mount("/blog", WSGIMiddleware(falcon_app))

