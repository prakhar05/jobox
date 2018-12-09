import logging
from flask import Flask,request
from flask_restful import Api
from resources.qa import Qa
from resources.question import Question, QuestionList
from resources.answer import Answer
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r'/*': {"origins": '*'}})
#CORS(app)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

#logging.basicConfig(filename='flask.log',level=logging.DEBUG)
#logging.getLogger('flask_cors').level = logging.DEBUG

#initialise DB
@app.before_first_request
def create_tables():
    db.create_all()

#@app.before_request
#def log_request_info():
#    app.logger.debug('Headers: %s', request.headers)
#    app.logger.debug('Body: %s', request.get_data())

#@app.after_request
#def after_request(response):
    #response.headers.add('Content-Type','application/json')
    #response.headers.add('Access-Control-Allow-Origin', 'null')
    #response.headers.add('Access-Control-Allow-Headers', 'content-type')
    #response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#    app.logger.debug('Response is')
#    app.logger.debug(response.headers)
#    return response
#    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')

#Set resource routes here
api.add_resource(Qa,'/qa', endpoint='qa')
api.add_resource(Qa,'/qa/<int:qa_id>',endpoint='qa_id')
api.add_resource(Question,'/question/<int:qa_id>', endpoint='question')
api.add_resource(Answer,'/answer/<int:question_id>', endpoint='answer')
api.add_resource(QuestionList,'/qa/<int:qa_id>/questions', endpoint='questions')


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=8080,debug=True)
