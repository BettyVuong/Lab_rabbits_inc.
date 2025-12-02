from src.services.db_service import db
from src.models import Question, Choice, Quiz, Quiz_Question, Elo, User, Review_Deck, TeacherStudent, Teacher


def add_student_to_teacher(student_id,teacher_id):

    check = db.session.get(TeacherStudent,{"teacher_id":teacher_id,"student_id":student_id})
    if check:
        return
    to_add = TeacherStudent(teacher_id = teacher_id, student_id = student_id)
    db.session.add(to_add)
    db.session.commit()