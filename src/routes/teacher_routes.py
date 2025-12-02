# linking students to teachers profile, to see stats of student level of elo
# create quizzes for students
# try quizzes without recording performance into db
# dashboard linking to teacher profile
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from src.services.db_service import db
from src.models import Quiz, Question, Choice
from src.services.llm_service import compute_student_clusters
from src.services.quiz_service import get_quiz_info
from src.services.quiz_service import get_teacher_quiz_info
from src.services.llm_service import update_student
from src.services.llm_service import mix_for_next_quiz
#from src.routes.quiz_routes import create_quiz_question_table
teacher_bp = Blueprint('teacher', __name__)
#create_quiz_bp = Blueprint('teacher', __name__)

@teacher_bp.route('/create_quiz/<int:teacher_id>', methods = ["GET"])
def create_quiz(teacher_id):

    return render_template("create_quiz.html",teacher_id=teacher_id)

@teacher_bp.route("/create_quiz/<int:teacher_id>", methods=["POST"])
def save_quiz(teacher_id):
    title = request.form.get("title")
    overall_diff = request.form.get("difficulty")
    diff_map = {"easy": 1, "medium": 2, "hard": 3}
    quiz_diff = diff_map.get(overall_diff)
    unit = "Class Quizzes"
    quiz = Quiz(title = title, difficulty=quiz_diff,teacher_id=teacher_id, unit = unit)

    db.session.add(quiz)
    db.session.flush()

    question_titles = {}
    question_diffs = {}

    i = 0
    for token in request.form:
        if "questions" in token and "text" in token:
            question_titles[i] = request.form.get(f"questions[{i}][text]")
            question_diffs[i] = int(request.form.get(f"questions[{i}][difficulty]"))
            i+=1


    for j in sorted(question_titles.keys()):
        q_title = question_titles[j]
        q_diff = question_diffs[j]

        question = Question(question=q_title,difficulty=q_diff,quiz_id=quiz.id, unit=unit)
        db.session.add(question)
        db.session.flush()

        choices = request.form.getlist(f"questions[{j}][choices][]")

        first = True
        for text in choices:
            if not text or not text.strip():
                continue

            ch = Choice(question_id=question.id,choice_text=text,is_correct=first)
            db.session.add(ch)
            first = False

    class_of_students = db.session.execute(db.text("SELECT student_id FROM teachers_students WHERE teacher_id =:id"), {"id": teacher_id}).mappings().fetchall()

    for row in class_of_students:
        db.session.execute(db.text("INSERT INTO elo (user_id, unit, rating, quiz_id)VALUES (:user_id, :unit, 1000, :quiz_id) ON CONFLICT DO NOTHING"), {"user_id": row["student_id"], "unit": unit, "quiz_id": quiz.id})

    db.session.commit()
    flash('Quiz created successfully!', 'success')
    return redirect(url_for('teacher_dashboard.teacher_dashboard', user_id=teacher_id))


@teacher_bp.route('/stats/<int:user_id>')
def stats(user_id):
    class_stats = return_classroom_stats(user_id)
    return render_template('student_statistics.html', class_stats=class_stats, teacher_id=user_id)

# gets a student id and then returns the specific student's statistics
def return_student_stats(student_id):
    # makes the database call to returns the student stats
    student_stats = [dict(row) for row in db.session.execute(db.text("SELECT unit, rating FROM elo WHERE user_id = :id"),{"id": student_id}).mappings().fetchall()]

    # changes the elo numbers into readable words to describe them
    for unit in student_stats:
        if unit['rating'] <= 800:
            unit['rating'] = 'At risk'
        elif (unit['rating'] > 800) and (unit['rating'] <= 900):
            unit['rating'] = 'Below standards'
        elif (unit['rating'] > 900) and (unit['rating']) <= 1050:
            unit['rating'] = 'At standards'
        elif unit['rating'] > 1050:
            unit['rating'] = 'Above standards'

    # returns the stats as a dictinary
    return student_stats

# Checks if a student is at risk: returns True if they are and False if they are not at risk
def check_at_risk(student_stats):
    ratings = set()
    # adds all of the ratings into a set from the student stats
    for stat in student_stats:
        ratings.add(stat['rating'])

    # since it is a set there are no duplicates so if the only element is at risk then the student is at risk
    if ratings == {'At risk'}:
        return True
    else:
        return False

# returns a single student name
def return_student_name(user_id):
    #gets the student name from the id
    name = db.session.execute(db.text("SELECT name FROM users WHERE id =:id"), {"id": user_id}).mappings().fetchone()

    # returns the name as a dictinary
    return name

def return_student_email(user_id):
    #gets the student email from the id
    email = db.session.execute(db.text("SELECT email FROM users WHERE id =:id"), {"id": user_id}).scalar()

    # returns the email as a string
    return email

def return_student_img(user_id):
    #gets the student img from the id
    img = db.session.execute(db.text("SELECT avatar FROM users WHERE id =:id"), {"id": user_id}).mappings().fetchone()

    # returns the avatar as a dictinary
    return img

# Is given a teacher_id and then returns a list of student names
def list_student_names(user_id):
    class_names = []
    #gets the ids from the joint table
    class_of_students = db.session.execute(db.text("SELECT student_id FROM teachers_students WHERE teacher_id =:id"), {"id": user_id}).mappings().fetchall()

    # loops through the students and adds their names to a list
    for student in class_of_students:
        student_name = return_student_name(student['name'])
        class_names.append(student_name)

    # returns a list of dictnaries of the student names
    return class_names


# gets a teacher's id and then returns the stats for each student in their class
def return_classroom_stats(user_id):
    class_stats = []
    # gets the student id's from the teachers class
    class_of_students = compute_student_clusters(user_id)

    #print(f"Hello {class_of_students}")
    # loops through the class to get the names and stats of each student
    for student in class_of_students:
        student_id = student['student_id']
        student_stats = return_student_stats(student_id)
        student_name = return_student_name(student_id)
        student_img = return_student_img(student_id)
        student_email = return_student_email(student_id)
        class_stats.append({
            "student_id": student_id,
            "name": student_name['name'],
            "email": student_email,
            "img": student_img['avatar'],
            "cluster_label": student['cluster_label'],
            "stats": student_stats
        })

    # returns the class as a list of dictinaries that contain a name dictinary then the cluster label dictinary and stats dictinary for the name
    return class_stats

@teacher_bp.route('/add_student/<string:email>/<int:teacher_id>', methods=['POST'])
# gets a student emial and a teacher id to add a student into the class
def add_email_to_id(email, teacher_id):
    try:
        student_id = db.session.execute(db.text("SELECT id FROM users WHERE email = :email"),{"email": email}).scalars().one()
    except Exception:
        flash('Student not found with that email', 'error')
        return redirect(url_for('teacher_dashboard.teacher_dashboard', user_id=teacher_id))
    
    if student_id is None:
        flash('Student not found with that email', 'error')
        return redirect(url_for('teacher_dashboard.teacher_dashboard', user_id=teacher_id))
    
    result = add_student(student_id, teacher_id)
    if result:
        flash('Student already enrolled with this teacher', 'error')
        return redirect(url_for('teacher_dashboard.teacher_dashboard', user_id=teacher_id))
    
    flash('Student added successfully', 'success')
    return redirect(url_for('teacher_dashboard.teacher_dashboard', user_id=teacher_id))

# gets a teacher and student id to add the student into the class
def add_student(student_id, teacher_id):
    # checks to see if the student is already in the class
    existing = db.session.execute(db.text("SELECT 1 FROM teachers_students WHERE student_id = :student_id AND teacher_id = :teacher_id"),{"student_id": student_id, "teacher_id": teacher_id}).first()

    if existing:
        return True  # Return True if student already exists

    # if it is a new student add them
    db.session.execute(db.text("INSERT INTO teachers_students (student_id, teacher_id) VALUES (:student_id, :teacher_id)"),{"student_id": student_id, "teacher_id": teacher_id})
    # get the teacher's quiz info
    quiz_info = db.session.execute(db.text("SELECT id, title FROM quiz WHERE teacher_id =:id"), {"id": teacher_id}).mappings().fetchall()

    # add the quiz info into the student info
    for quiz in quiz_info:
        add_id = quiz['id']
        add_title = quiz['title']
        db.session.execute(db.text("INSERT INTO elo (user_id, unit, rating, quiz_id) VALUES (:user_id, :unit, :rating, :quiz_id)"),{"user_id": student_id, "unit": add_title, "rating": 1000, "quiz_id": add_id})
    
    #commit all changes at once instead of after each operation
    db.session.commit()
    return False  #return False if student was successfully added

@teacher_bp.route('/delete_quiz/<int:teacher_id>/<int:quiz_id>', methods=['POST'])
# gets a teacher id and quiz id to delete the quiz and all related data
def delete_quiz(teacher_id, quiz_id):
    # Verify the quiz belongs to the teacher
    quiz = db.session.execute(db.text("SELECT id FROM quiz WHERE id = :quiz_id AND teacher_id = :teacher_id"),{"quiz_id": quiz_id, "teacher_id": teacher_id}).first()
    
    if not quiz:
        flash('Quiz not found or you do not have permission to delete it', 'error')
        return redirect(url_for('teacher_dashboard.teacher_dashboard', user_id=teacher_id))
    
    # Delete ELO records associated with this quiz
    db.session.execute(db.text("DELETE FROM elo WHERE quiz_id = :quiz_id"),{"quiz_id": quiz_id})
    
    # Get all question IDs for this quiz before deleting
    question_ids = db.session.execute(db.text("SELECT id FROM question WHERE quiz_id = :quiz_id"),{"quiz_id": quiz_id}).scalars().all()
    
    # Delete choices for questions in this quiz (cascade should handle this, but being explicit)
    if question_ids:
        db.session.execute(db.text("DELETE FROM choice WHERE question_id IN :question_ids"),{"question_ids": tuple(question_ids)})
    
    # Delete questions for this quiz
    db.session.execute(db.text("DELETE FROM question WHERE quiz_id = :quiz_id"),{"quiz_id": quiz_id})
    
    # Delete the quiz itself (this will cascade delete Quiz_Question and Teacher_Quiz records)
    db.session.execute(db.text("DELETE FROM quiz WHERE id = :quiz_id"),{"quiz_id": quiz_id})
    
    db.session.commit()
    flash('Quiz deleted successfully', 'success')
    return redirect(url_for('teacher_dashboard.teacher_dashboard', user_id=teacher_id))

@teacher_bp.route('/test_quiz/<int:teacher_id>/<int:quiz_id>/<int:elo>')
# page for the teacher to try out the quiz
def test_quiz(teacher_id, quiz_id, elo):
    # Clear any existing questions for this quiz_id to ensure clean state
    db.session.execute(db.text("DELETE FROM teacher_quiz WHERE quiz_id = :quiz_id AND user_id = :user_id"), {"quiz_id": quiz_id, "user_id": teacher_id})
    db.session.commit()
    
    #get difficulty distribution for quiz
    quizLevel = db.session.execute(db.text("SELECT difficulty FROM quiz WHERE id = :quiz_id"), {"quiz_id": quiz_id}).mappings().fetchone()
    quizLevel = quizLevel['difficulty']

    quiz_question_num = {}
    #determine num of questions for each level difficulty based on teacher chosen difficulty
    if quizLevel == 1: #elo level 900
        quiz_question_num = mix_for_next_quiz(elo, 10)
    elif quizLevel == 2: #elo level 1000
        quiz_question_num = mix_for_next_quiz(elo, 15)
    elif quizLevel == 3: #elo level 1100 max limit
        quiz_question_num = mix_for_next_quiz(elo, 20)
    else:
        return "Quiz not found", 404

    #create quiz in database
    create_quiz_question_table(teacher_id, quiz_id, quiz_question_num)

    #see quiz_service.py for more info
    quiz = get_teacher_quiz_info(quiz_id)

    if not quiz:
        return "Quiz not found", 404
    return render_template('test_quiz.html', teacher_id=teacher_id, quiz=quiz, elo=elo)

#inserts questions into quiz_question table for each user algo and difficulty
def create_quiz_question_table(user_id, quiz_id, quiz_question_num):
    # Actual implementation would depend on the database schema and requirements
    pos = 0
    #accessing values from the algorithm dictionary
    values = quiz_question_num.values()
    values_list = list(values)

    #number of questions for each difficulty
    easyNum = values_list[0]
    mediumNum = values_list[1]
    hardNum = values_list[2]

    # selecting total of ^ questions for each difficulty, random and no duplicates
    # IMPORTANT: Filter by quiz_id to only get questions that belong to this specific quiz
    question_result_easy = db.session.execute(db.text("SELECT id FROM question WHERE difficulty = 900 AND quiz_id = :quiz_id AND id NOT IN (SELECT question_id FROM teacher_quiz WHERE quiz_id = :quiz_id) ORDER BY RANDOM() LIMIT :easyNum"), { "quiz_id": quiz_id, "easyNum": easyNum}).scalars().all()
    question_result_medium = db.session.execute(db.text("SELECT id FROM question WHERE difficulty = 1000 AND quiz_id = :quiz_id AND id NOT IN (SELECT question_id FROM teacher_quiz WHERE quiz_id = :quiz_id) ORDER BY RANDOM() LIMIT :mediumNum"), { "quiz_id": quiz_id, "mediumNum": mediumNum}).scalars().all()
    question_result_hard = db.session.execute(db.text("SELECT id FROM question WHERE difficulty = 1100 AND quiz_id = :quiz_id AND id NOT IN (SELECT question_id FROM teacher_quiz WHERE quiz_id = :quiz_id) ORDER BY RANDOM() LIMIT :hardNum"), {"quiz_id": quiz_id, "hardNum": hardNum}).scalars().all()

    #loop through each difficulty and number of questions
    #loop for easy
    for i in range(len(question_result_easy)):
        question_id = question_result_easy[i]
        pos += 1
        #insert into teacher_quiz table
        db.session.execute(db.text("INSERT INTO teacher_quiz (quiz_id, question_id, pos, user_id)VALUES(:quiz_id, :question_id, :pos, :user_id) ON CONFLICT (quiz_id, question_id) DO NOTHING"), {"quiz_id": quiz_id, "question_id": question_id, "pos": pos, "user_id": user_id})
        db.session.commit()

    #loop for medium
    for i in range(len(question_result_medium)):
        question_id = question_result_medium[i]
        pos += 1
        #insert into teacher_quiz table
        db.session.execute(db.text("INSERT INTO teacher_quiz (quiz_id, question_id, pos, user_id)VALUES(:quiz_id, :question_id, :pos, :user_id) ON CONFLICT (quiz_id, question_id) DO NOTHING"), {"quiz_id": quiz_id, "question_id": question_id, "pos": pos, "user_id": user_id})
        db.session.commit()

    #loop for hard
    for i in range(len(question_result_hard)):
        question_id = question_result_hard[i]
        pos += 1
        #insert into teacher_quiz table
        db.session.execute(db.text("INSERT INTO teacher_quiz (quiz_id, question_id, pos, user_id)VALUES(:quiz_id, :question_id, :pos, :user_id) ON CONFLICT (quiz_id, question_id) DO NOTHING"), {"quiz_id": quiz_id, "question_id": question_id, "pos": pos, "user_id": user_id})
        db.session.commit()
    return

#insert for quiz submissions
@teacher_bp.route("/submit_test_quiz/<int:quiz_id>/<int:teacher_id>", methods=["POST"])
def submit_test_quiz(quiz_id, teacher_id):
    user_id = teacher_id#temp user_id, will fix on second iteration
    user_input = {}
    numOfQ = len(request.form)
    user_answers = []

    # quiz info
    #temp return to quiz result page
    quiz_id = 1
    quizTitle = db.session.execute(db.text("SELECT title FROM quiz WHERE id = :quiz_id"), {"quiz_id": quiz_id}).scalar()

    # every quiz has 10-20 questions, 1 mark each
    #get difficulty distribution for quiz
    quizLevel = db.session.execute(db.text("SELECT difficulty FROM quiz WHERE id = :quiz_id"), {"quiz_id": quiz_id}).mappings().fetchone()
    quizLevel = quizLevel['difficulty']

    totalMarks = 0
    #determine num of questions for each level difficulty based on teacher chosen difficulty
    if quizLevel == 1: #elo level 900
        totalMarks = 10
    elif quizLevel == 2: #elo level 1000
        totalMarks = 15
    elif quizLevel == 3: #elo level 1100 max limit
        totalMarks = 20
    else:
        return "Quiz not found", 404

    userMarks = 0

    #getting quiz input from front end submission
    for token, val in request.form.items():
        question_id = int(token.split("_")[1]) # getting question id
        user_input[question_id] = val # getting user input

        #getting question id, correct choice id, question text, correct choice text
        correct_answer = db.session.execute(db.text("SELECT q.id, c.id, c.is_correct, q.question, c.choice_text FROM question q JOIN choice c on q.id = c.question_id WHERE q.id = :question_id AND c.is_correct = true"), {"question_id": question_id}).mappings().fetchone()

        # has question id and text, user input and the correct answer text
        user_answers.append({
            "qId": question_id,
            "qText": correct_answer["question"],
            "answer": user_input[question_id],
            "correctAnswer": correct_answer["choice_text"]
        })

        # user choice and correct choice strings (if correct should be the same)
        userChoiceStr = user_input[question_id]
        correctChoiceStr = correct_answer["choice_text"]

        #alloc the correct unit name

        if userChoiceStr == correctChoiceStr:
            userMarks += 1 # if correct, 1 more mark

    # calculating final grade for quiz
    totalGrade = (userMarks / totalMarks) * 100

    quiz = {
        "id": quiz_id,
        "title": quizTitle,
        "numOfQ": numOfQ,
        "grade": totalGrade
    }

    #drop table teacher_quiz after submission for  new iterations and to prevent cluttering the db
    db.session.execute(db.text("DELETE FROM teacher_quiz WHERE user_id = :user_id"), {"user_id": user_id})
    db.session.commit()

    return render_template("results.html",quiz=quiz,user_id=user_id,user_answers=user_answers)

#to exit and delete quiz data
@teacher_bp.route('/exit_demo/<int:teacher_id>', methods=["POST"])
def exit_quiz(teacher_id):
    #drop table teacher_quiz after submission for  new iterations and to prevent cluttering the db
    db.session.execute(db.text("DELETE FROM teacher_quiz WHERE user_id = :user_id"), {"user_id": teacher_id})
    db.session.commit()

    return redirect(url_for('teacher_dashboard.teacher_dashboard', user_id=teacher_id))
