from flask_restful import Resource, reqparse
from models.qa import QaModel


class Qa(Resource):
    ##define request parser and fields to be parsed from the request body
    parser = reqparse.RequestParser()
    parser.add_argument('session_name')
    parser.add_argument('host_name',
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('start_time',
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('end_time',
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self,qa_id):
        qa_session = QaModel.get_by_id(qa_id)

        if qa_session:
            return qa_session.json()
        return {"message":"The QA session was not found"}, 404

    ##POST method
    def post(self):
        ##Parse arguments from request and store in 'request_data'
        request_data = Qa.parser.parse_args()

        ##if no session name gives, define a default name
        if not request_data["session_name"]:
            request_data["session_name"] = request_data["host_name"]+"'s session"

        ##validate start and endtime can be converted to time
        if not QaModel.validate_time(request_data["start_time"],request_data["end_time"]):
            return {"message":"Please enter valid UTC epoch time string for start_time and end_time where start_time < end_time"}, 400

        ##Create a QA session object using the parsed request_data
        qa_session = QaModel(**request_data)

        ##Save to DB
        try:
            qa_session.save_to_db()
        except:
            return {"message": "An error occurred creating the session."}, 500

        ##Return json representation of object
        return qa_session.json(),201
