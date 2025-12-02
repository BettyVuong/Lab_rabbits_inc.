#add code here
from src.services.db_service import db

from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    #idk what fields we want, maybe grade too
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    grade = db.Column(db.Integer, nullable = False, server_default="6" )
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable = False)
    avatar = db.Column(db.String(100))



class Question(db.Model):
    __tablename__ = 'question'


    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.Integer)
    unit = db.Column(db.String(100))


    quiz_id = db.Column(db.Integer,server_default="1",nullable=False)

class Choice(db.Model):
    __tablename__ = 'choice'
    id = db.Column(db.Integer, primary_key=True)
    #points to the id of the question it is related to
    question_id = db.Column(db.Integer, db.ForeignKey("question.id", ondelete="CASCADE"), nullable=False)
    choice_text = db.Column(db.Text, nullable = False)
    is_correct = db.Column(db.Boolean, nullable = False, default = False)

class Quiz(db.Model):
    __tablename__ = 'quiz'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    can_view = db.Column(db.Boolean, default=False, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False, server_default="2")
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=True)
    unit = db.Column(db.String(100))


class Quiz_Question(db.Model):
    __tablename__ = 'quiz_question'

    #pair it to a quiz id
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id", ondelete="CASCADE"), primary_key=True)

    #pair this to a question
    question_id = db.Column(db.Integer, db.ForeignKey("question.id", ondelete="CASCADE"), primary_key=True)

    #position of the question in the order, can be deleted
    pos = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, nullable=True)

class Teacher_Quiz (db.Model):
    __tablename__ = 'teacher_quiz'

    #pair it to a quiz id
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id", ondelete="CASCADE"), primary_key=True)

    #pair this to a question
    question_id = db.Column(db.Integer, db.ForeignKey("question.id", ondelete="CASCADE"), primary_key=True)

    #position of the question in the order, can be deleted
    pos = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, nullable=True)


class Review_Deck(db.Model):
    __tablename__ = 'review_deck'

    #pair it to a quiz id
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id", ondelete="CASCADE"), primary_key=True)

    #pair this to a question
    question_id = db.Column(db.Integer, db.ForeignKey("question.id", ondelete="CASCADE"), primary_key=True)

    #position of the question in the order, can be deleted
    pos = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, nullable=True)


class Elo(db.Model):
    __tablename__ = "elo"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"),primary_key=True)
    unit = db.Column(db.String(100), primary_key=True)
    rating = db.Column(db.Integer, nullable=False, server_default="1000")
    quiz_id  = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=True)

class Quiz_Results(db.Model):
    __tablename__ = "quiz_result"

    # id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"),primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id", ondelete="CASCADE"),primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id", ondelete="CASCADE"),primary_key=True)
    answer = db.Column(db.Boolean, nullable=False)

    # id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id", ondelete="CASCADE"), nullable=False)
    # question_id = db.Column(db.Integer, db.ForeignKey("question.id", ondelete="CASCADE"), nullable=False)
    # answer = db.Column(db.Boolean, nullable=False)


class Quiz_Mark(db.Model):
    __tablename__ = "quiz_mark"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"),primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id", ondelete="CASCADE"),primary_key=True)
    mark = db.Column(db.Integer, nullable=False)


class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable = False)
    avatar = db.Column(db.String(100))


class TeacherStudent(db.Model):
    __tablename__ = "teachers_students"

    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id", ondelete="CASCADE"),primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"),primary_key=True)