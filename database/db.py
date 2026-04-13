import mysql.connector
from config import DB_CONFIG

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Register User
def register_user(name, email, password):
    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, email, password))

    conn.commit()
    conn.close()

import mysql.connector
from config import DB_CONFIG

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def get_questions(semester, subject, unit):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT 
    question,
    COUNT(*) as frequency,
    GROUP_CONCAT(year) as year
    FROM questions
    WHERE semester=%s AND subject=%s AND unit=%s
    GROUP BY question
    ORDER BY frequency DESC
    """

    cursor.execute(query, (semester, subject, unit))
    data = cursor.fetchall()
    conn.close()
    return data

def log_visitor(ip, agent):
    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO visitors (ip_address, user_agent) VALUES (%s,%s)"
    cursor.execute(query, (ip, agent))

    conn.commit()
    conn.close()

def save_feedback(question, message):
    conn = get_connection()
    cursor = conn.cursor()

    query="INSERT INTO feedback(question,message) VALUES(%s,%s)"
    cursor.execute(query,(question,message))

    conn.commit()
    conn.close()


def get_important_questions():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query="""
    SELECT question, COUNT(*) as freq
    FROM questions
    GROUP BY question
    HAVING freq>=2
    ORDER BY freq DESC
    """

    cursor.execute(query)
    data=cursor.fetchall()
    conn.close()
    return data
def check_user(email, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE email=%s AND password=%s"
    cursor.execute(query, (email, password))

    user = cursor.fetchone()
    conn.close()

    return user