# Lab 3
**Goal:**
1. Finalize requirements for your Intelligent Tutoring System (ITS).
2. Identify use cases that emerge from those requirements.
3. Start creating a paper prototype for early usability testing.

## Part 1 - Finalize Requirements


### Must
| ReqID | Category | User |      Requirement      | Dependencies | Priority | TimeEstimate |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Must | The System | The System Must provide an easy-to-understand and engaging website interface so elementary students can navigate and learn independently. | 1 | 30 | 0.5 |
| 2 | Must | The System | The System Must provide a login mechanism to identify the Student’s profile and load the correct associated database for secure and personalized access. | 2 | 10 | 0.5 |
| 3 | Must | The System | The System Must be able to create quizzes from questions in the learning materials to provide Students with tailored assessments that reflect their learning content. | 3 | 10 | 0.5 |
| 4 | Must | The Student | The Student Must be able to access the home/landing page from anywhere on the site so navigation remains simple | 1 | 10 | 0.5 |
| 5 | Must | The System | The System Must tag each question with a difficulty to allow for appropriate quizzes to be generated based on the users progress. | 3 | 10 | 0.5 |
| 6 | Must | The System | The System Must tag each question with a topic and subtopic to allow for questions to be sorted and used appropriately in the right quizzes and modules. | 3 | 10 | 0.5 |
| 7 | Must | The System | The System Must analyze the Student’s quiz performance against the difficulty tags on each question to determine their level of understanding for measurable adaptive learning. | 5 | 10 | 1 |
| 8 | Must | The System | The System Must auto-save student progress on quizzes, so students don't lose progress in case of a technical failure. | 5 | 10 | 0.5 |
| 9 | Must | The System | The System Must securely store Student quiz attempts, scores, and responses for record-keeping and analytics. | 5 | 10 | 0.5 |
| 10 | Must | The System | The System Must indicate when a user gets a question wrong, so they have clarity of what topics/subtopics they need to focus on. | 3 | 10 | 0.5 |
| 11 | Must | The System | The System Must be able to sort the quizzes based on uncompleted to completed to allow the student to easily navigate and see what is left to complete | 3 | 5 | 0.5 |
| 12 | Must | The System | The System Must ensure that the site has a consistent and easy to understand header and footer with simple navigation options so students don't get confused. | 4 | 10 | 0.5 |
| 13 | Must | The Student | The Student Must be able to view their current progress levels for enrolled subtopics to track progress and identify areas for improvement. | 3 | 10 | 0.5 |
| 14 | Must | The Systemn | The System Must show large, clear, and concise warning messages when a student tries to change something on the site (for example change password) so that young students do not make any changes/mistakes they didnt want to make. | 1 | 10 | 0.5 |
| 15 | Must | The System | The System Must be able to store and save multiple Student profiles containing general information, and progress to maintain accurate records and support personalized learning. | 2 | 10 | 1 |


### Should
||||||||
| --- | --- | --- | --- | --- | --- | --- |
| 16 | Should | The System | The System Should provide students with timed quizzes if they choose so the quizzes feel more like in-class tests.  | 3 | 30 | 0.5 |
| 17 | Should | The System | The System Should allow students to choose the length of a practice quiz so they can fit learning time into their schedules  | 3 | 30 | 0.5 |
| 18 | Should | The Student | The Student Should be able to filter out or skip content they already know to avoid redundancy and use their study time more effectively. | 3 | 40 | 0.5 |
| 19 | Should | The System | The System Could provide a "recently attempted" panel on the main page so students can easily jump back into what they were doing lately with one simple click | 4 | 40 | 0.5 |
| 20 | Should | The System | The System Should provide clear and consise feedback for questions the student got wrong, rather than just the system saying it's wrong, so that the student can understand why they are wrong.  | 3 | 40 | 0.5 |
| 21 | Should | The System | The System Should be able to set recommended due dates or deadlines for certain modules to keep the student on schedule so that they do not fall behind. | 4 | 40 | 0.5 |
| 22 | Should | The System | The System Should provide accsessibility options such as enlarged fonts so students with diverse learning needs can fully engage with the tutoring system | 1 | 40 | 1 |
| 23 | Should | The System | The System Should periodically provide motivational messages when students have completed quizzes or whole units so they stay encouraged to learn or do not get discouraged | 1 | 40 | 0.5 |
| 24 | Should | The Student | The Student Should be allowed to restart quizzes they are stuck on or had to step away from so it is fair | 3 | 40 | 0.5 |
| 25 | Should | The System | The System Should recommend follow-up quizzes based on the student’s performance on previous quizzes, so that students can either progress to new content or review material that needs improvement. | 3 | 40 | 0.5 |
| 26 | Should | The Student | The Student Should be able to add notes in the quizzes making it so that they can have an easier time revisiting content for studying. | 3 | 40 | 0.5 |


### Could
||||||||
| --- | --- | --- | --- | --- | --- | --- |
| 27 | Could | The System | The System Could be able to hide units/quizzes and open them at certain times so that students cant work ahead of what they are learning in class. | 3 | 40 | 0.5 |
| 28 | Could | The Student | The Student Could be able to choose dark mode or light mode for better accessibility. | 1 | 40 | 0.5 |
| 29 | Could | The System | The System Could notify students by email when new content (quizzes or units) becomes available to keep them updated and engaged in their learning and progress. | 2 | 40 | 0.5 |
| 30 | Could | The System | The System Could remember login credentials within a specified timeframe, so students don't lose a lot of time logging in when unnecessary  | 2 | 40 | 0.5 |
| 31 | Could | The System | The System Could reduce brute-force guessing by reintroducing previously failed questions later in the quiz so that students cannot rely on immediate feedback to guess the correct answers. | 3 | 40 | 0.5 |
| 32 | Could | The System | The System Could provide alternate explanations or additional elaboration on difficult topics when a student struggles to understand the initial solution, so that they have multiple ways to grasp the material. | 3 | 40 | 1 |
| 33 | Could | The Student | The Student Could be able to switch between multiple types of learning such as quizzes, games, reading, etc., so that they have variety or can choose how they learn the best. | 4 | 40 | 0.5 |
| 34 | Could | The System | The System Could generate flashcards from questions students answered incorrectly to review concepts and reinforce learning in a way other than quizzes, which some students may appreciate. | 7 | 40 | 1 |
| 35 | Could | The System | The System Could send individualized progress reports to Students to provide direct feedback or guidance over long periods of time (semesters, school years, etc.) | 7 | 40 | 1 |


### Wont
||||||||
| --- | --- | --- | --- | --- | --- | --- |
| 36 | Won't | The System | The System Won't share any information other than what the student has agreed to in order to ensure everyone's privacy is respected and to avoid discouraging students | 2 |  | 0.5 |
| 37 | Won't | The System | The System Won't allow students to go back and change answers to avoid cheating and unfairness.  | 3 |  | 0.5 |
| 38 | Won't | The Student | The Student Won't have any way to bypass login authentication to ensure all accounts and information remains secure | 2 |  | 0.5 |
| 39 | Won't | The System | The System Won't allow students to edit names of units or quizzes to ensure consistency for all users | 4 |  | 0.5 |
| 40 | Won't | The Student | The Student Won't get emails from the tutoring system unless they specifically request so that it respects privacy policies   | 1 |  | 0.5 |
| 41 | Won't | The System | The System Won't have a chatbot to answer the students questions so that everything stays simplified for elementary school students | 1 |  | 0.5 |
| 42 | Won't | The Student | The Student Won’t be able to delete grades they have received from a course to preserve academic records and grading integrity. | 3 |  | 0.5 |
| 43 | Won't | The Student | The Student Won’t be able to modify another Student’s submissions to ensure fairness and protect academic integrity. | 2 |  | 0.5 |
| 44 | Won't | The Student | The Student Won’t be able to view the full solutions to quiz questions before completing the quiz to prevent cheating and preserve assessment integrity. | 3 |  | 0.5 |
| 45 | Won't | The Student | The Student Won't be able to view units or quizzes from other grades they are not enrolled in | 1 |  | 0.5 |
