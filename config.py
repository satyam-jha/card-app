import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('cards.db') or \
        'sqlite:///' + os.path.join(basedir, 'cards.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "0apz$^jo!sbhn3)q_vh5-^ssqx=2u-)ydrtkz1!o5%rp72e0t-"