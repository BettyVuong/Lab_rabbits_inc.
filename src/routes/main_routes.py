from flask import Blueprint, render_template, url_for, redirect

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
# @main_bp.route('/dashboard/<int:user_id>')
# @main_bp.route('/go_to_dashboard/<int:user_id>')

def home():
    return render_template('landing_page.html')

#code to redirect to dashboard for demo purposes
@main_bp.route('/go_to_dashboard/<int:user_id>')
def go_to_dashboard(user_id):
    return redirect(url_for('dashboard.dashboard', user_id=user_id))

@main_bp.route('/go_to_teacher_dashboard/<int:teacher_id>')
def go_to_teacher_dashboard(teacher_id):
    return redirect(url_for('teacher_dashboard_bp.teacher_dashboard', user_id=teacher_id))