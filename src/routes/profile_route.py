from flask import Blueprint, flash, render_template, request, redirect, url_for
from src.services.db_service import db

profile_bp = Blueprint('profile', __name__)

#profile route for student
@profile_bp.route('/profile_student/<int:user_id>', methods=['GET', 'POST'])
def profile_student(user_id):
    #getting info for profile view and edit
    avatar_list = ['avatar1.jpg', 'avatar2.jpg', 'avatar3.jpg', 'avatar4.jpg', 'avatar5.jpg', 'avatar6.jpg', 'avatar7.jpg', 'avatar8.jpg', 'avatar9.jpg', 'avatar10.jpg']
    #get name
    profile = db.session.execute(db.text("SELECT name, avatar FROM users WHERE id = :user_id"), {"user_id": user_id}).mappings().fetchall()
    db.session.commit()
    if not profile:
        flash('User profile not found.')
        return redirect(url_for('dashboard.dashboard', user_id=user_id))
    else:
        name = profile[0]['name']
        avatar = profile[0]['avatar']
    
    #update profile info
    if request.method == 'POST':
        new_avatar = request.form.get('avatar')
        new_name = request.form.get('name')
        if new_avatar in avatar_list:
            avatar = new_avatar
            db.session.execute(db.text("UPDATE users SET avatar = :avatar WHERE id = :user_id"), {"avatar": avatar, "user_id": user_id})
            db.session.commit()
        if new_name is not name:
            name = new_name
            db.session.execute(db.text("UPDATE users SET name = :name WHERE id = :user_id"), {"name": name, "user_id": user_id})
            db.session.commit()
        flash('Profile changes saved successfully.')
    return render_template('profile.html', user_id=user_id, avatar_list=avatar_list, name=name, current_avatar=avatar, profile_type='student')

#profile route for teacher
@profile_bp.route('/profile_teacher/<int:user_id>', methods=['GET', 'POST'])
def profile_teacher(user_id):
    #getting info for profile view and edit
    avatar_list = ['avatar1.jpg', 'avatar2.jpg', 'avatar3.jpg', 'avatar4.jpg', 'avatar5.jpg', 'avatar6.jpg', 'avatar7.jpg', 'avatar8.jpg', 'avatar9.jpg', 'avatar10.jpg']
    #get name
    profile = db.session.execute(db.text("SELECT name, avatar FROM teachers WHERE id = :user_id"), {"user_id": user_id}).mappings().fetchall()
    db.session.commit()
    if not profile:
        flash('User profile not found.')
        return redirect(url_for('teacher_dashboard_bp.teacher_dashboard', user_id=user_id))
    else:
        name = profile[0]['name']
        avatar = profile[0]['avatar']
    #update profile info
    if request.method == 'POST':
        new_avatar = request.form.get('avatar')
        new_name = request.form.get('name')
        if new_avatar in avatar_list:
            avatar = new_avatar
            db.session.execute(db.text("UPDATE teachers SET avatar = :avatar WHERE id = :user_id"), {"avatar": avatar, "user_id": user_id})
            db.session.commit()
        if new_name is not name:
            name = new_name
            db.session.execute(db.text("UPDATE teachers SET name = :name WHERE id = :user_id"), {"name": name, "user_id": user_id})
            db.session.commit()
        flash('Profile changes saved successfully.')
    return render_template('profile.html', user_id=user_id, avatar_list=avatar_list, name=name, current_avatar=avatar, profile_type='teacher')