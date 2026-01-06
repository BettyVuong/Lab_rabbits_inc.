# Lab Rabbits ITS
A full-stack intelligent tutoring web application intended to support teachers and students who are using the Ontario Curriculum. With premade topics for elementary students to take quizzes and review material. Teachers can create classrooms, create quizzes, test quizzes, and monitor classroom progress and understanding of units. Students learn in an interactive way, where the quizzes and review are tailored towards each individual to reinforce effective learning.

## Local Development
Requirements
- Python 3.12
- pip
- virtualenv
## Setup
To run the program create a venv using ```python3 -m venv venv``` in CLI and then activate the venv using ```source venv/bin/activate``` for mac or ```venv\Scripts\activate``` in CLI. Install the dependency in CLI ```pip install -r requirements.txt```
Afterwards, ensure to create a .env file with the following template, be sure that the file is located on the outermost file structure where files such as "venv" or "README.md" are.
```FLASK_APP = src:create_app 
FLASK_DEBUG =1
SECRET_KEY = <insert key>
DATABASE_URL = <your local postgres connection string>```
You should be able to run the program now, in the venv CLI use ```python3 app.py```, the http link for the local host should appear, paste the link into a web browser and you should be able to test the demo.
