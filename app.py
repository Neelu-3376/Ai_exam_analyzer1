from flask import Flask, render_template, request
from database.db import get_questions, log_visitor
from database.db import register_user,check_user
from ai.ai_utils import get_ai_answer
from database.db import save_feedback,get_important_questions
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("login.html")


from database.db import register_user   # ye import bhi add karo

@app.route('/register', methods=['GET','POST'])
def register():

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        register_user(name, email, password)

        return "Registration Successful! Go to Login"

    return render_template("register.html")


@app.route('/dashboard')
def dashboard():
    data=get_important_questions()
    return render_template("dashboard.html",important=data)

@app.route('/questions')
def questions():
    semester = request.args.get('semester')
    subject = request.args.get('subject')
    unit = request.args.get('unit')

    data = get_questions(semester, subject, unit)

    return render_template("questions.html", questions=data)


@app.route('/result')
def result():
    return render_template("result.html")


@app.route('/answer')
def answer():
    question = request.args.get('q')
    semester = request.args.get('semester')
    subject = request.args.get('subject')
    unit = request.args.get('unit')
    lang = request.args.get('lang')   # ✅ language added

    answer = get_ai_answer(question, lang)  # ✅ lang pass

    questions = get_questions(semester, subject, unit)

    return render_template(
        "questions.html",
        questions=questions,
        selected_question=question,
        ai_answer=answer
    )

@app.route('/feedback',methods=['POST'])
def feedback():
    msg=request.form.get("feedback")
    q=request.form.get("question")
    save_feedback(q,msg)
    return "Thanks for feedback"
from database.db import check_user

@app.route('/login', methods=['POST'])
def login():

    email = request.form['email']
    password = request.form['password']

    user = check_user(email, password)

    if user:
        
        return render_template("dashboard.html")
    else:
        return "Invalid Email or Password ❌"
if __name__ == '__main__':
    app.run(debug=True)