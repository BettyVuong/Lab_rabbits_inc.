from flask import Blueprint, render_template, url_for, redirect
# from quiz_routes import quiz_page
#from src.models.user import User
from src.services.db_service import db
from src.routes.teacher_routes import return_classroom_stats

teacher_dashboard_bp = Blueprint('teacher_dashboard', __name__)
#creates a route for the dashboard
@teacher_dashboard_bp.route('/teacher_dashboard/<int:user_id>')

def teacher_dashboard(user_id):
    #fetches query from the User model
    resultUser = db.session.execute(db.text("SELECT * FROM teachers WHERE id = :id"), {"id": user_id}).mappings().fetchone()
   
    if not resultUser:
        return "User not found", 404
    
    if resultUser:
        user = {
            "id": resultUser["id"],
            "username": resultUser["name"],
            "email": resultUser["email"],
            "avatar": resultUser["avatar"]
        }

    #accessList = quizAccess("Flight")

    #when user model is fixed use this
    #users = users.query.get_or_404(user_id)

    average_name, total = average_student(user_id)    

    # Fetch quizzes created by this teacher
    teacher_quizzes = db.session.execute(
        db.text("SELECT * FROM quiz WHERE teacher_id = :teacher_id AND teacher_id IS NOT NULL"),
        {"teacher_id": user_id}
    ).mappings().fetchall()
    
    quizzes = [dict(row) for row in teacher_quizzes]

    #renders the dashboard.html template with the user data
    return render_template('teacher_dashboard.html', average_name=average_name, total=total, user=user, user_id=user_id, quizzes=quizzes)

def cluster_numbers(class_stats, word):
    count = sum(1 for d in class_stats if d.get("cluster_label") == word)
    return count

def average_student(user_id):
    # gets the classroom stats so that the dashbord can have the average student stats and number of students
    class_stats = return_classroom_stats(user_id)
    Beginner = cluster_numbers(class_stats, "Beginner")
    Intermediate = cluster_numbers(class_stats, "Intermediate")
    Advanced = cluster_numbers(class_stats, "Advanced")
    Expert = cluster_numbers(class_stats, "Expert")
    # puts the values into a dictinary to use the max function on
    numbers = {"Expert": Expert, "Advanced": Advanced, "Intermediate": Intermediate, "Beginner": Beginner}
    largest = max(numbers, key=numbers.get)
    return largest, (Beginner+Intermediate+Advanced+Expert)


