from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from src.services.db_service import db
from src.services.quiz_service import get_quiz_info
from src.services.llm_service import update_student
from src.services.llm_service import mix_for_next_quiz
import math
quiz_bp = Blueprint('quiz_page', __name__)
quiz_submit_bp = Blueprint('quiz_submit', __name__)

# for quiz page to take quiz
@quiz_bp.route('/quiz/<int:quiz_id>/<int:user_id>')
def quiz_page(quiz_id, user_id):

    #getting student elo for specific unit from db
    eloForUnit = db.session.execute(db.text("SELECT rating FROM elo WHERE user_id = :id AND quiz_id = :quiz_id"), {"id": user_id, "quiz_id": quiz_id}).mappings().fetchone()
    if eloForUnit is not None:
        eloForUnit = eloForUnit['rating']
    else:
        eloForUnit = 1000  #default ELO for new users

    #algorithm to get mix of questions for next quiz
    if eloForUnit < 980:
        quiz_question_num = mix_for_next_quiz(eloForUnit, 10)
    elif eloForUnit >= 980 and eloForUnit < 1080:
        quiz_question_num = mix_for_next_quiz(eloForUnit, 15)
    elif eloForUnit >= 1080:
        quiz_question_num = mix_for_next_quiz(eloForUnit, 20)
    else:
        return "Quiz level found", 404

    create_quiz_question_table(user_id, quiz_id, quiz_question_num)

    #see quiz_service.py for more info
    quiz = get_quiz_info(quiz_id)

    if not quiz:
        return "Quiz not found", 404
    
    return render_template("quiz_final.html", quiz=quiz, user_id=user_id)

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
    question_result_easy = db.session.execute(db.text("SELECT id FROM question WHERE difficulty = 900 AND quiz_id = :quiz_id AND id NOT IN (SELECT question_id FROM quiz_question WHERE quiz_id = :quiz_id) ORDER BY RANDOM() LIMIT :easyNum"), {"quiz_id": quiz_id, "easyNum": easyNum}).scalars().all()
    question_result_medium = db.session.execute(db.text("SELECT id FROM question WHERE difficulty = 1000 AND quiz_id = :quiz_id AND id NOT IN (SELECT question_id FROM quiz_question WHERE quiz_id = :quiz_id) ORDER BY RANDOM() LIMIT :mediumNum"), {"quiz_id": quiz_id, "mediumNum": mediumNum}).scalars().all()    
    question_result_hard = db.session.execute(db.text("SELECT id FROM question WHERE difficulty = 1100 AND quiz_id = :quiz_id AND id NOT IN (SELECT question_id FROM quiz_question WHERE quiz_id = :quiz_id) ORDER BY RANDOM() LIMIT :hardNum"), {"quiz_id": quiz_id, "hardNum": hardNum}).scalars().all()       

    #loop through each difficulty and number of questions
    #loop for easy
    for i in range(len(question_result_easy)):
        question_id = question_result_easy[i]
        pos += 1
        #insert into quiz_question table
        db.session.execute(db.text("INSERT INTO quiz_question (quiz_id, question_id, pos, user_id)VALUES(:quiz_id, :question_id, :pos, :user_id) ON CONFLICT (quiz_id, question_id) DO NOTHING"), {"quiz_id": quiz_id, "question_id": question_id, "pos": pos, "user_id": user_id})
        db.session.commit()
        
    #loop for medium
    for i in range(len(question_result_medium)):
        question_id = question_result_medium[i]
        pos += 1
        #insert into quiz_question table
        db.session.execute(db.text("INSERT INTO quiz_question (quiz_id, question_id, pos, user_id)VALUES(:quiz_id, :question_id, :pos, :user_id) ON CONFLICT (quiz_id, question_id) DO NOTHING"), {"quiz_id": quiz_id, "question_id": question_id, "pos": pos, "user_id": user_id})
        db.session.commit()
        
    #loop for hard
    for i in range(len(question_result_hard)):
        question_id = question_result_hard[i]
        pos += 1
        #insert into quiz_question table
        db.session.execute(db.text("INSERT INTO quiz_question (quiz_id, question_id, pos, user_id)VALUES(:quiz_id, :question_id, :pos, :user_id) ON CONFLICT (quiz_id, question_id) DO NOTHING"), {"quiz_id": quiz_id, "question_id": question_id, "pos": pos, "user_id": user_id})
        db.session.commit()
    return

#insert for quiz submissions
@quiz_bp.route("/submit_quiz/<int:quiz_id>/<int:user_id>", methods=["POST"])
#@quiz_submit_bp.route("/submit_quiz/<int:quiz_id>", methods=["POST"])
def submit_quiz(quiz_id, user_id):
    user_input = {}
    numOfQ = len(request.form)
    user_answers = []

    # quiz info
    #temp return to quiz result page        
    quizTitle = db.session.execute(db.text("SELECT title FROM quiz WHERE id = :quiz_id"), {"quiz_id": quiz_id}).scalar()
    
    # every quiz has 10 questions, 1 mark each
    totalMarks = 10 
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

        # updating student elo and databases quiz_result after each question
        #get student elo for unit
        student_elo = db.session.execute(db.text("SELECT rating FROM elo WHERE user_id = :user_id AND quiz_id = :quiz_id"), {"user_id": user_id, "quiz_id": quiz_id}).scalar()
        if student_elo is None:
            student_elo = 1000
        #get question elo
        question_elo = db.session.execute(db.text("SELECT difficulty FROM question WHERE id = :question_id"), {"question_id": question_id}).scalar()
        
        unit = db.session.execute(db.text("SELECT unit FROM quiz WHERE id = :quiz_id"), {"quiz_id": quiz_id}).mappings().fetchone()
        unit_name = unit['unit']
        
        if userChoiceStr == correctChoiceStr:
            userMarks += 1 # if correct, 1 more mark
            #update elo
            elo_update = update_student(student_elo, question_elo, True)
            #update student elo for unit in db
            db.session.execute(db.text("UPDATE elo SET rating = :elo_update WHERE user_id = :user_id AND quiz_id = :quiz_id"), {"elo_update": elo_update, "user_id": user_id, "quiz_id": quiz_id})
            db.session.commit()
        else:
        #comparing question answers with user input using queries
            elo_update = update_student(student_elo, question_elo, False)
            #update student elo for unit in db
            db.session.execute(db.text("UPDATE elo SET rating = :elo_update WHERE user_id = :user_id AND quiz_id = :quiz_id"), {"elo_update": elo_update, "user_id": user_id, "quiz_id": quiz_id})
            db.session.commit()

        db.session.execute(db.text("INSERT INTO quiz_result (user_id, quiz_id, question_id, answer)VALUES (:user_id, :quiz_id, :question_id, :answer)ON CONFLICT (user_id, quiz_id, question_id)DO UPDATE SET answer = EXCLUDED.answer"), {"user_id": user_id, "quiz_id": quiz_id, "question_id": question_id, "answer": True})
        db.session.commit()

    # calculating final grade for quiz
    totalGrade = (userMarks / totalMarks) * 100

    quiz = {
        "id": quiz_id,
        "title": quizTitle,
        "numOfQ": numOfQ,
        "grade": totalGrade
    }

    #insert final score into quiz_mark table db
    db.session.execute(db.text("INSERT INTO quiz_mark (user_id, quiz_id, mark)VALUES (:user_id, :quiz_id, :mark)ON CONFLICT (user_id, quiz_id)DO UPDATE SET mark = EXCLUDED.mark"), {"user_id": user_id, "quiz_id": quiz_id, "mark": totalGrade})
    db.session.commit()

    #drop table quiz_question after submission for  new iterations and to prevent cluttering the db
    db.session.execute(db.text("DELETE FROM quiz_question WHERE user_id = :user_id"), {"user_id": user_id})
    db.session.commit()

    return render_template("results.html",quiz=quiz,user_id=user_id,user_answers=user_answers)

#to exit and delete quiz data
@quiz_bp.route('/exit_quiz/<int:user_id>', methods=["POST"])
def exit_quiz(user_id):
    
    db.session.execute(db.text("DELETE FROM quiz_question WHERE user_id = :user_id"), {"user_id": user_id})
    db.session.commit()

    return redirect (url_for('dashboard.dashboard', user_id=user_id))

def get_quiz_attempt(userid, quizid):
    quiz_attempts = db.session.execute(db.text("SELECT qm.mark FROM quiz_mark qm JOIN quiz q ON qm.quiz_id = q.id WHERE qm.user_id = :user_id AND qm.quiz_id = :quiz_id"), {"user_id": userid, "quiz_id": quizid}).mappings().all()
    return quiz_attempts

@quiz_bp.route('/check_quiz_attempt/<int:quiz_id>/<int:user_id>')
def check_quiz_attempt(quiz_id, user_id):
    """Check if user has taken this quiz before"""
    quiz_attempts = get_quiz_attempt(user_id, quiz_id)
    has_attempt = quiz_attempts is not None and len(quiz_attempts) > 0
    return jsonify({"has_attempt": has_attempt})

@quiz_bp.route('/last_attempt/<int:quiz_id>/<int:user_id>')
def last_attempt(quiz_id, user_id):
    # Get the mark from quiz_mark table using get_quiz_attempt
    quiz_attempts = get_quiz_attempt(user_id, quiz_id)
    
    if not quiz_attempts or len(quiz_attempts) == 0:
        flash('No previous attempt found for this quiz', 'error')
        return redirect(url_for('dashboard.dashboard', user_id=user_id))
    
    # Get the last mark (most recent attempt)
    last_mark = quiz_attempts[-1]['mark']
    
    # Get quiz info
    quizTitle = db.session.execute(db.text("SELECT title FROM quiz WHERE id = :quiz_id"), {"quiz_id": quiz_id}).scalar()
    
    if not quizTitle:
        flash('Quiz not found', 'error')
        return redirect(url_for('dashboard.dashboard', user_id=user_id))
    
    # Get all questions answered in quiz_result table
    quiz_results = db.session.execute(db.text("SELECT question_id, answer FROM quiz_result WHERE user_id = :user_id AND quiz_id = :quiz_id"), {"user_id": user_id, "quiz_id": quiz_id}).mappings().all()
    
    user_answers = []
    numOfQ = 0
    
    # For each question in quiz_result, get question text and correct answer
    for result in quiz_results:
        question_id = result['question_id']
        was_correct = result['answer']
        
        # Get question text and correct answer
        correct_answer = db.session.execute(db.text("SELECT q.id, q.question, c.choice_text FROM question q JOIN choice c ON q.id = c.question_id WHERE q.id = :question_id AND c.is_correct = true"), {"question_id": question_id}).mappings().fetchone()
        
        if correct_answer:
            # If answer was correct, show correct answer as user's answer
            # If incorrect, show "Incorrect" as user's answer
            user_answer_text = correct_answer["choice_text"] if was_correct else "Incorrect"
            
            user_answers.append({
                "qId": question_id,
                "qText": correct_answer["question"],
                "answer": user_answer_text,
                "correctAnswer": correct_answer["choice_text"]
            })
            numOfQ += 1
    
    # Format quiz data similar to submit_quiz
    quiz = {
        "id": quiz_id,
        "title": quizTitle,
        "numOfQ": numOfQ,
        "grade": last_mark
    }
    
    return render_template("last_attempt.html", quiz=quiz, user_id=user_id, user_answers=user_answers)