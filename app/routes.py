from email import message
import json
from app import app , db
from flask import Flask, request, jsonify, make_response
from datetime import datetime, timedelta
from app.models import User, UserCard, card, Deck, to_collection_dict
from  werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
            print(data)
            current_user = User.query\
                .filter_by(id = data['id'])\
                .first()
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated


@app.route('/')
def index():
    return "Hello, N"
    

@app.route('/user', methods =['GET'])
@token_required
def get_all_users(current_user):
    # querying the database
    # for all the entries in it
    users = User.query.all()
    # converting the query objects
    # to list of jsons
    output = []
    for user in users:
        # appending the user data json
        # to the response list
        output.append({
            'public_id': user.public_id,
            'name' : user.name,
            'email' : user.email
        })
  
    return jsonify({'users': output})
  
# route for logging user in
@app.route('/login', methods =['POST'])
def login():
    # creates dictionary of form data
    auth = request.form
  
    if not auth or not auth.get('email') or not auth.get('password'):
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
        )
  
    user = User.query\
        .filter_by(email = auth.get('email'))\
        .first()
  
    if not user:
        # returns 401 if user does not exist
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
        )
  
    if check_password_hash(user.password_hash, auth.get('password')):
        # generates the JWT Token
        token = jwt.encode({
            'id': user.id,
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, app.config['SECRET_KEY'])
        user_data = user.to_dict()
        user_data['token'] = token
        return make_response(jsonify({'user': user_data}), 201)
    # returns 403 if password is wrong
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
    )
  
# signup route
@app.route('/signup', methods =['POST'])
def signup():
    # creates a dictionary of the form data
    data = request.form
  
    # gets name, email and password
    name, email = data.get('name'), data.get('email')
    password = data.get('password')
  
    # checking for existing user
    user = User.query\
        .filter_by(email = email)\
        .first()
    if not user:
        # database ORM object
        user = User(
            username = name,
            email = email,
            password_hash = generate_password_hash(password)
        )
        # insert user
        db.session.add(user)
        db.session.commit()
        token = jwt.encode({
            'id': user.id,
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, app.config['SECRET_KEY'])
        user_data = user.to_dict()
        user_data['token'] = token

        return make_response(jsonify({'user' : user_data, 'message':'Successfully registered.'}), 201)
    else:
        # returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)


@app.route('/decks', methods =['GET'])
@token_required
def get_decks(current_user):
    decks = to_collection_dict(Deck.query.all())
    return make_response({'decks': decks}, 200)

@app.route('/decks', methods =['POST'])
@token_required
def create_decks(current_user):
    data = request.form
    decks = Deck(
        name=data.get('name')
    )
    db.session.add(decks)
    db.session.commit()
    return make_response({'decks': decks.to_dict()}, 200)


@app.route('/card', methods=['POST'])
@token_required
def add_cards(current_user):
    data = request.form
    cards = []
    card_data, deck_id = data.get('cards'), data.get('deck')
    card_data = json.loads(card_data)

    for data in card_data:
        new_card = card(
            question = data['question'],
            answer = data['answer'],
            deck_id = deck_id,
            order = data['order'],
        )

        db.session.add(new_card)
        db.session.commit()
        cards.append(new_card)



    return make_response({'Data':to_collection_dict(cards)}, 200)

