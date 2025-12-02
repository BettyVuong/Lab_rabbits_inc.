from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash
from datetime import datetime, timezone
from sqlalchemy import func
from src.services.db_service import db
from src.models import User, Teacher

#0 for success 1 for fail
def check_hash(hashedstr,str):
    ph = PasswordHasher()
    try:
        ph.verify(hashedstr.strip(), str)
        return 0
    except (VerifyMismatchError, InvalidHash):
        return 1


#can move these nums around later
#0 for valid
#1 email already exists in db
#2 passwords entered do not match
#3 password does not meet requirements (missing digit, too short, or missing special char)

def create_account(name, email, password_a1, password_a2): 
    # Check DB for email, if email does not exist proceed
    # Else (email exists in db) return 1
    existing_user = db.session.execute(db.text("SELECT id, 'user' AS type FROM users WHERE email = :email UNION ALL SELECT id, 'teacher' AS type FROM teachers WHERE email = :email"),
        {"email": email}).fetchone()

    if(existing_user):
        return 1

    # Check if both attempts at entering password were the same
    if(password_a1 != password_a2):
        return 2
    
    # Check for password constraints, checks for a digit, length, and special char
    special_chars = "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~"

    if not (any(char.isdigit() for char in password_a1)):#digit
        return 3
    elif len(password_a1)<8:#length
      return 3
    elif not any(char in special_chars for char in password_a1):#special char
        return 3
    
    ph = PasswordHasher()
    pass1hash = ph.hash(password_a1)
    created_at = datetime.now(timezone.utc)   # UTC timestamp
    grade = 6  #default grade level 
    #query to insert the hashed password and other info as new user into table
    query_result = db.session.execute(
        db.text("""
            INSERT INTO users (name, email, password, created_at, grade, avatar)
            VALUES (:name, :email, :password, :created_at, :grade, :avatar)
            RETURNING id
        """),
        {
            "name": name,
            "email": email,
            "password": pass1hash,
            "created_at": created_at,
            "grade": grade
            ,"avatar": 'avatar1.jpg'
        }
    ).mappings().fetchone()
    # set up required joins
    new_user_id = query_result["id"]
    units = ["Biodiversity", "Electricity", "Flight", "Solar System"]
    default_elo = 1000
    for unit in units:
        db.session.execute(
            db.text("""
                INSERT INTO elo (user_id, unit, rating)
                    VALUES (:user_id, :unit, :rating)
                """),
                {
                    "user_id": new_user_id,
                    "unit": unit,
                    "rating": default_elo,
                }
            )

    db.session.commit()
    return 0

#return 0 if successful, 1 if the email does not exist, 2 if email exists but password doesnt
def verify_login(email, password):
    #dummy for now can be changed based on how the query is structured
    ph = PasswordHasher()
    query_result = db.session.execute(
        db.text(""" 
            SELECT * FROM users WHERE email = :email
        """),
        {"email": email}
    ).mappings().fetchone()

    if query_result == None:
        return 1

    fetched_email = query_result["email"]
    fetched_password = query_result["password"]
    #if email found
    # hash_curr_pass = ph.hash(password) #pretty sure this is unecessary since argon does this step for you
    #check if the password is corrected
    if(check_hash(fetched_password,password)==0):
        return 0
    else:
        return 2

    return 0



def verify_teacher_login(email, password):
    #dummy for now can be changed based on how the query is structured
    ph = PasswordHasher()
    query_result = db.session.execute(
        db.text(""" 
            SELECT * FROM teachers WHERE email = :email
        """),
        {"email": email}
    ).mappings().fetchone()

    if query_result == None:
        return 1

    fetched_email = query_result["email"]
    fetched_password = query_result["password"]
    #if email found
    # hash_curr_pass = ph.hash(password) #pretty sure this is unecessary since argon does this step for you
    #check if the password is corrected
    if(check_hash(fetched_password,password)==0):
        return 0
    else:
        return 2

    return 0


#can move these nums around later
#0 for valid
#1 email already exists in db
#2 passwords entered do not match
#3 password does not meet requirements (missing digit, too short, or missing special char)

def create_teacher_account(name, email, password_a1, password_a2): 
    # Check DB for email, if email does not exist proceed
    # Else (email exists in db) return 1
    existing_user = db.session.execute(
        db.text("""
        SELECT id, 'user' AS type FROM users WHERE email = :email
        UNION ALL
        SELECT id, 'teacher' AS type FROM teachers WHERE email = :email
        """),
        {"email": email}
    ).fetchone()

    if(existing_user):
        return 1

    # Check if both attempts at entering password were the same
    if(password_a1 != password_a2):
        return 2
    
    # Check for password constraints, checks for a digit, length, and special char
    special_chars = "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~"

    if not (any(char.isdigit() for char in password_a1)):#digit
        return 3
    elif len(password_a1)<8:#length
      return 3
    elif not any(char in special_chars for char in password_a1):#special char
        return 3
    
    ph = PasswordHasher()
    pass1hash = ph.hash(password_a1)
    created_at = datetime.now(timezone.utc)   # UTC timestamp
    #query to insert the hashed password and other info as new user into table
    query_result = db.session.execute(
        db.text("""
            INSERT INTO teachers (name, email, password, created_at, avatar)
            VALUES (:name, :email, :password, :created_at, :avatar)
            RETURNING id
        """),
        {
            "name": name,
            "email": email,
            "password": pass1hash,
            "created_at": created_at
            ,"avatar": 'avatar1.jpg'
        }
    ).mappings().fetchone()
    db.session.commit()
    return 0

def get_user_id(email):
    userid = db.session.execute(db.text(" SELECT id FROM users WHERE email = :email "), {"email": email}).mappings().fetchone()
    if userid:
        return userid["id"]
    else:
        return None
    
def get_teacher_id(email):
    userid = db.session.execute(db.text(" SELECT id FROM teachers WHERE email = :email "), {"email": email}).mappings().fetchone()
    if userid:
        return userid["id"]
    else:
        return None