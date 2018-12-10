from datetime import datetime
from db import db


class QaModel(db.Model):
    ##Define DB table and columns
    __tablename__ = 'qasession'
    id = db.Column(db.Integer, primary_key=True)
    session_name = db.Column(db.String(200),nullable=False)
    host_name = db.Column(db.String(80),nullable=False)
    start_time = db.Column(db.DateTime,nullable=False)
    end_time = db.Column(db.DateTime,nullable=False)
    question = db.relationship('QuestionModel',backref='qasession',lazy=True)

    ##Convert timestamp string to utc datetime object
    def __init__(self,session_name,host_name,start_time,end_time):
        self.session_name = session_name
        self.host_name = host_name
        self.start_time = datetime.utcfromtimestamp(int(start_time))
        self.end_time = datetime.utcfromtimestamp(int(end_time))

    ##Get QA session by id
    @classmethod
    def get_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    ##Validate start_time and end_time values
    @classmethod
    def validate_time(cls,start_time,end_time):
        now = datetime.utcnow()
        try:
            starttime = datetime.utcfromtimestamp(int(start_time))
            endtime = datetime.utcfromtimestamp(int(end_time))
        except:
            return False

        if endtime <= starttime:
            return False

        return True

    ##Check if session is ongoing based on its start and end time, and time of request
    def is_ongoing(self):
        now = datetime.utcnow()
        return True if (now >= self.start_time) and (now <= self.end_time) else False

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    ##Return object details with start and end time as readable utc format "YYYY/MM/DD HH:MM:SS z"
    def json(self):
        return {'id':self.id,
                'session_name':self.session_name,
                'host_name':self.host_name,
                'start_time':self.start_time.strftime('%Y/%m/%d %H:%M:%Sz'),
                'end_time':self.end_time.strftime('%Y/%m/%d %H:%M:%Sz')}
