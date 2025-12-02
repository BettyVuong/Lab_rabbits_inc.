from flask import Blueprint, flash, render_template, request, redirect, url_for
from src.services.auth_service import create_account, verify_login, verify_teacher_login, create_teacher_account, get_user_id, get_teacher_id

auth_bp = Blueprint('auth', __name__)

#login route for students
@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        data = request.form
        email = data.get('email')
        password = data.get('password')
        login_result = verify_login(email, password)
        #get id and route to dashboard if valid
        if login_result == 0:
            #getting user id
            userid = get_user_id(email)
            if userid:
                return redirect (url_for('main.go_to_dashboard', user_id=userid))
            else:
                flash('No account was found, please try again.')
                return render_template('login_student.html')#should not happen, error in database
        elif login_result == 1:
            flash('Email doesn\'t exist. Please try again.')
        elif login_result == 2:
            flash('Email exists but password doesn\'t. Please try again.')
        else:
            flash('Login failed due to an unknown error. Please try again.')
    return render_template('login_student.html')

#register account route for students
@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        data = request.form
        name = data.get('name')
        email = data.get('email')
        password_a1 = data.get('password_a1')
        password_a2 = data.get('password_a2')
        register_result = create_account(name, email, password_a1, password_a2)
        if register_result == 0:
            userid = get_user_id(email)
            if userid:
                return redirect (url_for('main.go_to_dashboard', user_id=userid))
            else:
                flash('No account was found, please try again.')
                return render_template('register_student.html')#should not happen, error in database
        elif register_result == 1:
            flash('An account with this email already exists. Please use a different email.')
        elif register_result == 2:
            flash('Passwords do not match. Please try again.')
        elif register_result == 3:
            flash('Password must be at least 8 characters long and contain at least one digit and one special character.')
        else:
            flash('Registration failed due to an unknown error. Please try again.')
    return render_template('register_student.html')

#teacher login route
@auth_bp.route('/teacher_login', methods=['GET','POST'])
def teacher_login():
    if request.method == 'POST':
        data = request.form
        email = data.get('email')
        password = data.get('password')
        login_result = verify_teacher_login(email, password)
        if login_result == 0:
            #getting user id
            userid = get_teacher_id(email)
            if userid:
                #change this to teacher dashboard later
                return redirect(url_for('teacher_dashboard.teacher_dashboard', user_id=userid))
            else:
                flash('No account was found, please try again.')
                return render_template('login_teacher.html')#should not happen, error in database
        elif login_result == 1:
            flash('Email doesn\'t exist. Please try again.')
        elif login_result == 2:
            flash('Email exists but password doesn\'t. Please try again.')
        else:
            flash('Login failed due to an unknown error. Please try again.')

    return render_template('login_teacher.html')

#teacher register route
@auth_bp.route('/teacher_register', methods=['GET','POST'])
def teacher_register():
    if request.method == 'POST':
        data = request.form
        name = data.get('name')
        email = data.get('email')
        password_a1 = data.get('password_a1')
        password_a2 = data.get('password_a2')
        register_result = create_teacher_account(name, email, password_a1, password_a2)
        if register_result == 0:
            userid = get_teacher_id(email)
            if userid:
                #change this to teacher dashboard later
                return redirect(url_for('teacher_dashboard.teacher_dashboard', user_id=userid))
            else:
                flash('No account was found, please try again.')
                return render_template('register_teacher.html')#should not happen, error in database
        elif register_result == 1:
            flash('An account with this email already exists. Please use a different email.')
        elif register_result == 2:
            flash('Passwords do not match. Please try again.')
        elif register_result == 3:
            flash('Password must be at least 8 characters long and contain at least one digit and one special character.')
        else:
            flash('Registration failed due to an unknown error. Please try again.')
    return render_template('register_teacher.html')
