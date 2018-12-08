from flask import Flask
from flask_restful import Api
from resources.qa import Qa
from resources.question import Question, QuestionList
from resources.answer import Answer

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

#initialise DB
@app.before_first_request
def create_tables():
    db.create_all()

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
