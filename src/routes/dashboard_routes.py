from flask import Blueprint, render_template, url_for, redirect
from src.services.db_service import db

dashboard_bp = Blueprint('dashboard', __name__)
#creates a route for the dashboard
@dashboard_bp.route('/dashboard/<int:user_id>')

def dashboard(user_id):
    #fetches query from the User model
    resultUser = db.session.execute(db.text("SELECT * FROM users WHERE id = :id"), {"id": user_id}).mappings().fetchone()

    #for future not fixed id use this
    #resultUser = db.session.execute(db.text("SELECT * FROM users WHERE id = :id"), {"id": user_id}).mappings().fetchone()
   
    if not resultUser:
        return "User not found", 404
    
    if resultUser:
        user = {
            "id": resultUser["id"],
            "username": resultUser["name"],
            "email": resultUser["email"],
            "grade": resultUser["grade"],
            "avatar": resultUser["avatar"]
        }

    teachers = db.session.execute(db.text("SELECT t.name AS name FROM teachers t JOIN teachers_students ts ON ts.teacher_id = t.id WHERE ts.student_id = :user_id"), {"user_id": user_id}).mappings().fetchall()
    teacherList = [t['name'] for t in teachers]
    teachersId = db.session.execute(db.text("SELECT t.id AS id FROM teachers t JOIN teachers_students ts ON ts.teacher_id = t.id WHERE ts.student_id = :user_id"), {"user_id": user_id}).mappings().fetchall()
    teacherIdList = [t['id'] for t in teachersId]

    allQuizzes = db.session.execute(db.text("SELECT * FROM quiz")).mappings().fetchall()
    shownQuizzes = []

    for row in allQuizzes:
        teacher_id = row['teacher_id']
        if teacher_id is None:
            shownQuizzes.append(dict(row))
        else:
            # if student is enrolled to that specific teacher shown that quiz on dashboard
            if teacher_id in teacherIdList:
                shownQuizzes.append(dict(row))
        # if teacher_id is null, dont show in dashboard

    for i, quiz in enumerate(shownQuizzes):
        quiz_id = quiz['id']
        accessList = quizAccess(quiz_id, user_id)
        shownQuizzes[i]['accessList'] = accessList

    #when user model is fixed use this
    #users = users.query.get_or_404(user_id)

    #renders the dashboard.html template with the user data
    return render_template('dashboard.html', user=user, user_id=user_id, teacherList=teacherList, quizzes=shownQuizzes)

def quizAccess(quiz_id, user_id):
    studentElo = db.session.execute(db.text("SELECT rating FROM elo WHERE user_id = :id AND quiz_id = :quiz_id"), {"id": user_id, "quiz_id": quiz_id}).mappings().fetchone()
    if studentElo is not None:
        studentElo = studentElo["rating"]
    else:
        studentElo = 1000

    canAccess = [True, False, False]
    
    #changed to lock quiz 2
    if studentElo > 1000 and studentElo < 1080:
        canAccess[1] = True
    
    if studentElo >= 1080:
        canAccess[1] = True
        canAccess[2] = True

    return canAccess

def go_to_quiz(user_id,quiz_id):
    return redirect(url_for('quiz_bp.quiz_page', quiz_id=quiz_id))

def go_to_review(user_id,quiz_id):
    return redirect(url_for('review_page.review_page', quiz_id=quiz_id))