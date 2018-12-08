from db import db

class QuestionModel(db.Model):
    ##Define DB table and columns
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    qa_id = db.Column(db.Integer, db.ForeignKey('qasession.id'),nullable=False)
    asked_by_user = db.Column(db.String(80),nullable=False)
    answer_text = db.Column(db.Text,nullable=True)
    answer_image_url = db.Column(db.Text,nullable=True)
    answer_by_user = db.Column(db.String(80),nullable=True)

    def __init__(self,qa_id,text,asked_by_user):
        self.qa_id = qa_id
        self.text = text
        self.asked_by_user = asked_by_user

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_db(self):
        db.session.commit()

    def add_answer(self,answer_text,answer_image_url,answer_by_user):
        self.answer_text = answer_text
        self.answer_image_url = answer_image_url
        self.answer_by_user = answer_by_user

    ##Check if answer already exists for a question
    def is_answered(self):
        if not self.answer_text and not self.answer_image_url and not self.answer_by_user:
            return False
        else:
            return True

    ##Return matching questions
    @classmethod
    def question_exists(cls,text,asked_by_user):
        return cls.query.filter(cls.text==text,cls.asked_by_user==asked_by_user).first()

    ##return questions based on question_id
    @classmethod
    def get_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    ##return all questions based on session id, and filter 
    @classmethod
    def get_all_by_id(cls,qa_id,type):
        if type==None or type=="all":
            return cls.query.filter(cls.qa_id==qa_id)
        elif type=="answered":
            return cls.query.filter(cls.qa_id==qa_id, cls.answer_by_user!=None)
        elif type=="unanswered":
            return cls.query.filter(cls.qa_id==qa_id, cls.answer_by_user==None)

    def json(self):
        return {"id":self.id,
                "QA_session_id":self.qa_id,
                "Text":self.text,
                "Asked_by":self.asked_by_user,
                "answer_text":self.answer_text,
                "answer_image_url":self.answer_image_url,
                "answer_by_user":self.answer_by_user,
                }
