from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Volunteer(db.Model):
    __tablename__ = 'volunteers'
    volunteer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    phone_number = db.Column(db.String)

    def __init__(self, first_name, last_name, phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number


# def add_lesson(teacher_id, info):
#     teacher = User.query.filter_by(id=teacher_id, role=Role.TEACHER).first()
#     if not teacher: raise exceptions.TeacherDosentExistError()
#     lesson = Lesson(info=info, teacher=teacher)
#
#     db.session.add(lesson)
#     db.session.commit()
