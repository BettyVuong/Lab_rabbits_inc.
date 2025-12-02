####
from src.services.db_service import db
from src.models import Question, Choice, Quiz, Quiz_Question, Elo, User, Review_Deck, Teacher_Quiz

import csv

def create_elo_for_all_users_based_on_teacher_id_and_quiz_id(teacher_id, quiz_id, unit):
    class_of_students = db.session.execute(db.text("SELECT student_id FROM teachers_students WHERE teacher_id =:id"), {"id": teacher_id}).mappings().fetchall()

    for row in class_of_students:
        db.session.execute(db.text("INSERT INTO elo (user_id, unit, rating, quiz_id)VALUES (:user_id, :unit, 1000, :quiz_id) ON CONFLICT DO NOTHING"), {"user_id": row["student_id"], "unit": unit, "quiz_id": quiz_id})
    db.session.commit()


def create_elo_for_user(user_id):
    for unit in ["Flight", "Electricity"]:
        db.session.add(Elo(user_id=user_id, unit=unit, rating = 1000))
    db.session.commit()

def create_user_temp():

    email = "test1231@gmail.ca"
    user = User.query.filter_by(email=email).first()

    if user:
        return user.id

    user = User(name = "123 23234",email=email,password= "hello")
    db.session.add(user)
    db.session.commit()
    create_elo_for_user(user.id)

    return user.id





#q,a,wa,wa,wa,difficulty

def add_csv_to_db(file):

    with open(file, newline = '') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            q = Question(question = row[0], difficulty = row[5], unit = "Solar System", quiz_id = 4)
            db.session.add(q)
            #flush assigns and id
            db.session.flush()

            if row[1] == 'T' or row[1] == 'F':
                db.session.add(Choice(question_id = q.id, choice_text = row[1], is_correct = True))
                db.session.add(Choice(question_id = q.id, choice_text = row[2], is_correct = False))
                continue
            db.session.add(Choice(question_id = q.id, choice_text = row[1], is_correct = True))
            db.session.add(Choice(question_id = q.id, choice_text = row[2], is_correct = False))
            db.session.add(Choice(question_id = q.id, choice_text = row[3], is_correct = False))
            db.session.add(Choice(question_id = q.id, choice_text = row[4], is_correct = False))
    db.session.commit()



# https://flask-sqlalchemy.readthedocs.io/en/stable/queries/
# https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html

#make a question, including the choices
def make_question(question, choices, correct_index, difficulty):
    q = Question(question = question, difficulty = difficulty)
    db.session.add(q)
    db.session.flush()

    for i, choice_text in enumerate(choices):
        db.session.add(Choice(question_id = q.id, choice_text = choice_text, is_correct = (i == correct_index)))

    db.session.commit()
    return q.id

#create a quiz
def create_quiz(title):
    quiz = Quiz(title = title, can_view=False)
    db.session.add(quiz)
    db.session.commit()
    return quiz.id

#put a question inside of a quiz (doesnt actually move the question), pos is the position of the question in the quiz
def put_question_in_quiz(quiz_id,question_id,pos):

    to_add = Quiz_Question(quiz_id = quiz_id, question_id = question_id, pos = pos)
    db.session.add(to_add)
    db.session.commit()

#non destructive, it wont delete a question itself, only from the quiz
def remove_question_from_quiz(quiz_id, question_id):
    connection = db.session.get(
        (Quiz_Question, {"quiz_id": quiz_id, "question_id": question_id})
    )

    if not connection:
        return False
    db.session.delete(connection)
    db.session.commit()
    return True

#change the location of a question in a quiz by pos
def reorder_quiz_by_question(quiz_id, question_id, position):
    connection = db.session.get(Quiz_Question,{"quiz_id": quiz_id, "question_id": question_id})
    if not connection:
        return False
    connection.pos = position

    db.session.commit()


#Following format
#quiz id, quiz title
#questions, questionid1, questionText
#choices, choicesid's, choiceText's
#does not return if a choice is correct
#example
#{'id': 1, 'title': 'Test Quiz', 'questions': [{'id': 1, 'question': 'You cannot see, taste or smell the air around you unless it is polluted.', 'choices': {'id': [1, 2], 'text': ['T', 'F']}}, {'id': 2, 'question': 'Aerodynamics is the study of water in motion', 'choices': {'id': [3, 4], 'text': ['T', 'F']}}]}


def get_quiz_info(quiz_id):
    quiz = db.session.get(Quiz, quiz_id)

    if not quiz:
        return None

    #return questions and choices


    questions = db.session.execute(db.select(Quiz_Question).filter_by(quiz_id=quiz_id).order_by(Quiz_Question.pos, Quiz_Question.question_id)).scalars().all()

    out = {"id": quiz.id, "title": quiz.title, "questions": []}

    # tracks the num of questions so frontend can use it
    numOfQ = 0

    #i is of type quiz question
    for i in questions:
        # type question
        question = db.session.get(Question, i.question_id)

        if not question:
            continue

        choice =  db.session.execute(db.select(Choice).where(Choice.question_id == question.id).order_by(db.func.random())).scalars().all()

        # same thing as numOfQ but for choices
        numOfC = 0

        choices = {"id":[], "text": []}
        for c in choice:
            choices["id"].append(c.id)
            choices["text"].append(c.choice_text)
            numOfC += 1


        out["questions"].append({
            "id": question.id,
            "question": question.question,
            "difficulty": question.difficulty,
            "choices": choices,
            "numOfC": numOfC
        })

        numOfQ += 1

    out["numOfQ"] = numOfQ

    return out


# def get_quiz_info_slidedeck(quiz_id):
#     quiz = db.session.get(Quiz, quiz_id)

#     if not quiz:
#         return None

#     #return questions and choices

#     questions = db.session.execute(db.select(Question).filter_by(quiz_id=quiz_id).order_by(Review_Deck.pos, Review_Deck.question_id)).scalars().all()

#     out = {"id": quiz.id, "title": quiz.title, "questions": []}

#     # tracks the num of questions so frontend can use it
#     numOfQ = 0

#     #i is of type quiz question
#     for i in questions:
#         # type question
#         question = db.session.get(Question, i.question_id)

#         if not question:
#             continue

#         correctChoiceText = db.session.execute(db.text("SELECT q.id, c.id, c.is_correct, q.question, c.choice_text FROM question q JOIN choice c on q.id = c.question_id WHERE q.id = :question_id AND c.is_correct = true"), {"question_id": question.id}).mappings().fetchone()

#         # same thing as numOfQ but for choices
#         numOfC = 0

#         out["questions"].append({
#             "id": question.id,
#             "question": question.question,
#             "difficulty": question.difficulty,
#             "choice": correctChoiceText,
#             "numOfC": numOfC
#         })

#         numOfQ += 1

#     out["numOfQ"] = numOfQ

#     return out

def get_quiz_info_slidedeck(quiz_id):
    quiz = db.session.get(Quiz, quiz_id)

    if not quiz:
        return None

    #return questions and choices


    questions = db.session.execute(db.select(Review_Deck).filter_by(quiz_id=quiz_id).order_by(Review_Deck.question_id)).scalars().all()

    out = {"id": quiz.id, "title": quiz.title, "questions": []}

    # tracks the num of questions so frontend can use it
    numOfQ = 0

    #i is of type quiz question
    for i in questions:
        # type question
        question = db.session.get(Question, i.question_id)

        if not question:
            continue

        #choice  = (db.session.execute(db.select(Choice).where(Choice.question_id == question.id, Choice.is_correct == True)).scalars().all())
        correctChoiceText = db.session.execute(db.text("SELECT c.choice_text FROM question q JOIN choice c on q.id = c.question_id WHERE q.id = :question_id AND c.is_correct = true"), {"question_id": question.id}).mappings().fetchone()
        correctChoiceText = correctChoiceText["choice_text"]
        # same thing as numOfQ but for choices
        numOfC = 0


        out["questions"].append({
            "id": question.id,
            "question": question.question,
            "difficulty": question.difficulty,
            "choice": correctChoiceText,
            "numOfC": numOfC
        })

        numOfQ += 1

    out["numOfQ"] = numOfQ

    return out





def put_in_database():
    question1 = make_question(
        "You cannot see, taste or smell the air around you unless it is polluted.",
        ["T","F"],
        correct_index = 0,
        difficulty = 1
    )

    question2 = make_question(
        "Aerodynamics is the study of water in motion",
        ["T","F"],
        correct_index = 1,
        difficulty = 3
    )

    quiz_id = create_quiz("Test Quiz")
    put_question_in_quiz(quiz_id, question1, pos=1)
    put_question_in_quiz(quiz_id,question2,pos=2)
    return quiz_id

def get_teacher_quiz_info(quiz_id):
    quiz = db.session.get(Quiz, quiz_id)

    if not quiz:
        return None

    #return questions and choices


    questions = db.session.execute(db.select(Teacher_Quiz).filter_by(quiz_id=quiz_id).order_by(Teacher_Quiz.pos, Teacher_Quiz.question_id)).scalars().all()

    out = {"id": quiz.id, "title": quiz.title, "questions": []}

    # tracks the num of questions so frontend can use it
    numOfQ = 0

    #i is of type quiz question
    for i in questions:
        # type question
        question = db.session.get(Question, i.question_id)

        if not question:
            continue

        choice =  db.session.execute(db.select(Choice).where(Choice.question_id == question.id).order_by(Choice.id)).scalars().all()

        # same thing as numOfQ but for choices
        numOfC = 0

        choices = {"id":[], "text": [], "is_correct": []}
        for c in choice:
            choices["id"].append(c.id)
            choices["text"].append(c.choice_text)
            choices["is_correct"].append(c.is_correct)
            numOfC += 1


        out["questions"].append({
            "id": question.id,
            "question": question.question,
            "difficulty": question.difficulty,
            "choices": choices,
            "numOfC": numOfC
        })

        numOfQ += 1

    out["numOfQ"] = numOfQ

    return out