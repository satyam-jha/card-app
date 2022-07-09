
from flask import Flask, request, jsonify, make_response
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import jwt
from datetime import datetime, timedelta
from functools import wraps


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)



from app import models, routes

