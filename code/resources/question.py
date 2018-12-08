from flask_restful import Resource, reqparse
from models.question import QuestionModel
from models.qa import QaModel

class Question(Resource):
    ##define request parser and fields to be parsed from the request body
    parser = reqparse.RequestParser()
    parser.add_argument('text',
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('asked_by_user',
                        required=True,
                        help="This field cannot be left blank!"
                        )

    ##POST method
    def post(self,qa_id):
        session = QaModel.get_by_id(qa_id)

        ##If sesssion exists, is ongoing, and question doesnt exist, allow posting question, else error
        if session:
            if not session.is_ongoing():
                return {"message":"This session is not currently active"}, 400

            request_data = Question.parser.parse_args()

            if QuestionModel.question_exists(request_data["text"],request_data["asked_by_user"]):
                return {"message":"This question already exists for this session"}, 400

            question = QuestionModel(qa_id,request_data["text"],request_data["asked_by_user"])

            try:
                question.save_to_db()
            except Exception as e:
                print(str(e))
                return {"message": "An error occurred while posting the question."}, 500
        else:
            return {"message": "The session was not found"}, 404

        #return object json representation if request was successful
        return question.json(),201


class QuestionList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('type')

    ##GET method
    def get(self,qa_id):
        request_data = QuestionList.parser.parse_args()
        questions = QuestionModel.get_all_by_id(qa_id,request_data["type"])
        questions_list = [question.json() for question in questions]

        if questions_list != []:
            return {"Questions": questions_list}, 201
        else:
            return {"message": "No questions found. Check if session exists, or check your filter criteria"}, 404
