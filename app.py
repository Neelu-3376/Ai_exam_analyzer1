from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from ai.ai_utils import get_ai_answer
from database.db import (
    get_questions,
    register_user,
    check_user,
    get_important_questions,
    save_feedback,
    get_total_users,
    get_total_logs,
    get_connection
)
from flask import send_file
from pdf_generator import generate_pdf
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)


# --- 1. INITIAL ENTRY ---
@app.route('/')
def index():

    if 'user' in session:
        return redirect(url_for('dashboard'))

    return render_template("index.html")


# --- 2. AUTHENTICATION ---
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        user = check_user(email, password)

        if user:

            session['user'] = email

            admin_emails = [
                "rashmivishwakarma613@gmail.com",
                "neelut521@gmail.com"
            ]

            # ✅ Admin Login
            if email in admin_emails:
                return redirect(url_for('admin'))

            # ✅ Normal User Login
            return redirect(url_for('dashboard'))

        return "Invalid Email or Password ❌ <a href='/login'>Try again</a>"

    return render_template("login.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        try:

            register_user(
                name,
                email,
                password
            )

            return redirect(url_for('login'))

        except Exception as e:

            return f"Error: {e}"

    return render_template("signup.html")


# --- 3. DASHBOARD ---
@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template("dashboard.html")


@app.route('/admin')
def admin():

    admin_emails = [
        "rashmivishwakarma613@gmail.com",
        "neelut521@gmail.com"
    ]
    print("CURRENT USER:", session.get('user'))

    if 'user' not in session:
        return redirect(url_for('login'))

    if session.get('user') in admin_emails:

        total_users = get_total_users()
        total_logs = get_total_logs()

        return render_template(
            "admin.html",
            total_users=total_users,
            total_logs=total_logs
        )

    return "<h1>Unauthorized 🚫 Only Admin can access this.</h1>",403

# --- 5. API ENDPOINTS ---

@app.route('/api/subjects/<semester>')
def api_subjects(semester):

    sem_num = semester.replace(
        "Semester ",
        ""
    ).strip()

    subjects_data = {

        "1":[
            "Mathematics-I",
            "Engineering Chemistry",
            "English for Communication",
            "Engineering Graphics",
            "Basic Electrical & Electronics Engineering"
        ],

        "2":[
            "Mathematics-II",
            "Engineering Physics",
            "Basic Mechanical Engineering",
            "Basic Civil Engineering & Mechanics",
            "Basic Computer Engineering"
        ],

        "3":[
            "Energy & Environmental Engineering ",
            "Data Structure",
            "Discrete Structure",
            "Digital Systems",
            "Object Oriented Programming",
        ],

        "4":[
            "Analysis Design of Algorithm",
            "Software Engineering",
            "Operating System",
            "Computer Org. & Architecture",
            "Mathematics-III"
        ],

        "5":[
            "Theory of Computation",
            "Database Management Systems",
            "Pattern Recognition",
            "Internet and Web Technology"
        ],

        "6":[
            "Machine Learning",
            "Computer Networks",
            "Compiler Design",
            "Project Management"
        ]
    }

    return jsonify(
        subjects_data.get(
            sem_num,
            []
        )
    )


@app.route('/api/units/<subject>')
def api_units(subject):

    return jsonify([
        "Unit 1",
        "Unit 2",
        "Unit 3",
        "Unit 4",
        "Unit 5"
    ])


# QUESTIONS API
@app.route('/api/questions/<semester>/<subject>/<unit>')
def api_questions(
    semester,
    subject,
    unit
):

    try:

        print(f"[API] semester={semester}")
        print(f"[API] subject={subject}")
        print(f"[API] unit={unit}")

        data = get_questions(
            semester,
            subject,
            unit
        )

        formatted_data = []

        for item in data:

            repeat = item.get(
                'repeat_count',
                1
            )

            probability = min(
                95,
                60 + (repeat * 10)
            )

            formatted_data.append({

                "q": item['question'],
                "repeat": repeat,
                "probability": f"{probability}%"

            })

        print(
            f"[API] Returning {len(formatted_data)} questions"
        )

        return jsonify(
            formatted_data
        )

    except Exception as e:

        print(
            "API ERROR:",
            e
        )

        return jsonify({
            "error": str(e)
        }),500


# IMPORTANT QUESTIONS API
@app.route('/api/important/<subject>/<unit>')
def api_important(
    subject,
    unit
):

    try:

        data = get_important_questions(
            subject,
            unit
        )

        formatted_data = []

        for item in data:

            repeat = item.get(
                'repeat_count',
                1
            )

            probability = min(
                95,
                60 + (repeat * 10)
            )

            formatted_data.append({

                "q": item["question"],
                "repeat": repeat,
                "probability": f"{probability}%"

            })

        return jsonify(
            formatted_data
        )

    except Exception as e:

        print(
            "IMPORTANT API ERROR:",
            e
        )

        return jsonify({
            "error": str(e)
        }),500


# --- 6. AI ---
@app.route('/api/ask-ai', methods=['POST'])
def ask_ai():

    if 'user' not in session:

        return jsonify({
            "answer":"Login Required"
        }),403

    data = request.json

    answer = get_ai_answer(
        data.get('question'),
        data.get('mode','normal')
    )

    return jsonify({
        "answer":answer
    })


# --- 7. LOGOUT ---
@app.route('/logout')
def logout():

    session.clear()

    return redirect(
        url_for('index')
    )

@app.route('/logs')
def logs():

    if 'user' not in session:
        return redirect(url_for('login'))

    admin_emails = [
        "rashmivishwakarma613@gmail.com",
        "neelut521@gmail.com"
    ]

    if session.get('user') not in admin_emails:
        return "Unauthorized 🚫", 403

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM feedback
        ORDER BY id DESC
    """)

    logs = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "logs.html",
        logs=logs
    )

@app.route('/download-pdf/<subject>/<unit>')
def download_pdf(subject, unit):

    data = get_important_questions(
        subject,
        unit
    )

    questions = []

    for item in data:

        question = item['question']

        answer = get_ai_answer(
            question,
            "english"
        )

        questions.append({
            "question": question,
            "answer": answer
        })

    filename = f"{subject}_{unit}.pdf"

    generate_pdf(
        filename,
        questions
    )

    return send_file(
        filename,
        as_attachment=True
    )

@app.route('/users')
def users():

    if 'user' not in session:
        return redirect(url_for('login'))

    admin_emails = [
        "rashmivishwakarma613@gmail.com",
        "neelut521@gmail.com"
    ]

    if session.get('user') not in admin_emails:
        return "Unauthorized 🚫", 403

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, name, email
        FROM users
        ORDER BY id DESC
    """)

    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "users.html",
        users=users
    )
@app.route('/delete_logs', methods=['POST'])
def delete_logs():

    if 'user' not in session:
        return redirect(url_for('login'))

    admin_emails = [
        "rashmivishwakarma613@gmail.com",
        "neelut521@gmail.com"
    ]

    if session.get('user') not in admin_emails:
        return "Unauthorized 🚫", 403

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM feedback")

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('admin'))

@app.route('/papers/<subject>')
def papers(subject):

    folder_name = subject.replace(" ", "_")

    folder_path = os.path.join(
        'static',
        'papers',
        folder_name
    )

    print("FOLDER PATH:", folder_path)

    pdf_files = []

    if os.path.exists(folder_path):

        pdf_files = [

            f for f in os.listdir(folder_path)

            if f.lower().endswith('.pdf')

        ]

    print("PDF FILES:", pdf_files)

    return render_template(
        'papers.html',
        subject=subject,
        folder_name=folder_name,
        pdf_files=pdf_files
    )
if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
    app.run(debug=True)
