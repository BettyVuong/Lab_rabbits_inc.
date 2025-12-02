from flask import Blueprint, render_template, request, redirect, url_for
from src.services.db_service import db
from src.services.quiz_service import get_quiz_info_slidedeck
from src.services.quiz_service import get_quiz_info
from src.services.llm_service import update_student
import math
review_bp = Blueprint('review_page', __name__)

#algorithm for elo quiz creation and ml training
ANCHORS = {"easy": 900, "medium": 1000, "hard": 1100}


def difficulty_weights(student_elo: float, spread: float = 90.0):
    raw = {k: math.exp(-((student_elo - rq) ** 2) / (2 * spread ** 2)) for k, rq in ANCHORS.items()}
    total = sum(raw.values())
    return {k: raw[k] / total for k in raw}


def _alloc(weights: dict, quiz_len: int):
    floats = {k: weights[k] * quiz_len for k in weights}
    floors = {k: int(floats[k]) for k in floats}
    leftover = quiz_len - sum(floors.values())


    remainders = sorted(((floats[k] - floors[k], k) for k in floors), reverse=True)
    for _, k in remainders[:leftover]:
        floors[k] += 1
    return floors


def mix_for_next_quiz(student_elo: float, quiz_len: int, spread: float = 90.0):
    return _alloc(difficulty_weights(student_elo, spread), quiz_len)

# for quiz page to take quiz
@review_bp.route('/review/<int:quiz_id>/<int:user_id>')
def review_page(quiz_id, user_id):
    unit = db.session.execute(db.text("SELECT unit FROM quiz WHERE id = :quiz_id"), {"quiz_id": quiz_id}).mappings().fetchone()
    unit = unit['unit']
    
    #for flight unit do this algorithm generation
    #getting student elo for specific unit from db
    eloForUnit = db.session.execute(db.text("SELECT rating FROM elo WHERE user_id = :id AND quiz_id = :quiz_id"), {"id": user_id, "quiz_id": quiz_id}).mappings().fetchone()
    if eloForUnit is not None:
        eloForUnit = eloForUnit['rating']
    else:
        eloForUnit = 1000  #default ELO for new users
    #algorithm to get mix of questions for next quiz
    review_question_num = mix_for_next_quiz(eloForUnit, 10)
    create_info_slidedeck_table(user_id, quiz_id, unit, review_question_num)
    unit_name = unit

    #see quiz_service.py for more info
    review = get_quiz_info_slidedeck(quiz_id)

    if not review:
        return "Review not found", 404

    resultUser = db.session.execute(db.text("SELECT * FROM users WHERE id = :id"), {"id": user_id}).mappings().fetchone()
    if not resultUser:
        return "User not found", 404
    
    if resultUser:
        user = {
            "id": resultUser["id"],
            "username": resultUser["name"],
            "email": resultUser["email"],
            "grade": resultUser["grade"]
        }

    stats = {
        "completed_quizzes": 3,
        "average_score": 88,
        "time_spent": "2 hours"
    }
    
    return render_template("review_final.html", review=review, unit_name=unit_name, user=user, stats=stats, user_id=user_id)

#inserts questions into quiz_question table for each user algo and difficulty
def create_info_slidedeck_table(user_id, quiz_id, unit, quiz_question_num):
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
        #insert into review_deck table
        db.session.execute(db.text("INSERT INTO review_deck (quiz_id, question_id, pos, user_id)VALUES(:quiz_id, :question_id, :pos, :user_id) ON CONFLICT (quiz_id, question_id) DO NOTHING"), {"quiz_id": quiz_id, "question_id": question_id, "pos": pos, "user_id": user_id})
        db.session.commit()
        
    #loop for medium
    for i in range(len(question_result_medium)):
        question_id = question_result_medium[i]
        pos += 1
        #insert into review_deck table
        db.session.execute(db.text("INSERT INTO review_deck (quiz_id, question_id, pos, user_id)VALUES(:quiz_id, :question_id, :pos, :user_id) ON CONFLICT (quiz_id, question_id) DO NOTHING"), {"quiz_id": quiz_id, "question_id": question_id, "pos": pos, "user_id": user_id})
        db.session.commit()
        
    #loop for hard
    for i in range(len(question_result_hard)):
        question_id = question_result_hard[i]
        pos += 1
        #insert into review_deck table
        db.session.execute(db.text("INSERT INTO review_deck (quiz_id, question_id, pos, user_id)VALUES(:quiz_id, :question_id, :pos, :user_id) ON CONFLICT (quiz_id, question_id) DO NOTHING"), {"quiz_id": quiz_id, "question_id": question_id, "pos": pos, "user_id": user_id})
        db.session.commit()
    return

#insert for quiz submissions
@review_bp.route("/exit_review/<int:user_id>", methods=["POST"])
def exit_review(user_id):

    #drop table quiz_question after submission for  new iterations and to prevent cluttering the db
    db.session.execute(db.text("DELETE FROM review_deck WHERE user_id = :user_id"), {"user_id": user_id})
    db.session.commit()
    
    return redirect (url_for('dashboard.dashboard', user_id=user_id))