# coding: utf-8
from flask import Flask
from uploader.views import blueprint


def create_app():
    """Factory app"""
    app = Flask(__name__)
    app.config.from_object('uploader.local.Config')
    app.debug = app.config['DEBUG']
    app.register_blueprint(blueprint)
    return app