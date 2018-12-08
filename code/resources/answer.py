from flask_restful import Resource, reqparse
from models.question import QuestionModel

class Answer(Resource):
    ##define request parser and fields to be parsed from the request body
    parser = reqparse.RequestParser()
    parser.add_argument('text')
    parser.add_argument('image_url')
    parser.add_argument('answered_by',
                        required=True,
                        help="This field cannot be left blank!"
                        )

    ##POST method
    def post(self,question_id):
        request_data = Answer.parser.parse_args()

        ##Ensure either answer text or image url is provided
        if not request_data["text"] and not request_data["image_url"]:
            return {"message":"Both fields 'text' and 'image_url' cannot be empty."}, 400

        question = QuestionModel.get_by_id(question_id)

        ##Allow answering a question if not already answered
        if question and not question.is_answered():
            question.add_answer(request_data["text"],request_data["image_url"],request_data["answered_by"])
            try:
                question.update_db()
            except:
                return {"message": "An error occurred while posting the answer."}, 500
        else:
            return {"message":"The question does not exist, or has already been answered"}, 400

        return question.json(),201
