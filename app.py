from flask import Flask, render_template, request, redirect, url_for
from db_config import connection

app = Flask(__name__)

exam = {
    "title": "AWS Cloud Fundamentals",
    "questions": [
        {
            "question": "Which AWS service provides virtual servers?",
            "options": ["Amazon EC2", "Amazon S3", "Amazon RDS", "AWS Lambda"],
            "answer": "Amazon EC2"
        },
        {
            "question": "Which AWS service stores objects?",
            "options": ["Amazon EC2", "Amazon S3", "Amazon VPC", "IAM"],
            "answer": "Amazon S3"
        },
        {
            "question": "Which AWS service provides a relational database?",
            "options": ["SNS", "Amazon S3", "CloudFront", "Amazon RDS"],
            "answer": "Amazon RDS"
        },
        {
            "question": "Which AWS service distributes incoming traffic?",
            "options": ["Application Load Balancer", "IAM", "Route53", "CloudTrail"],
            "answer": "Application Load Balancer"
        },
        {
            "question": "Which AWS service automatically scales EC2 instances?",
            "options": ["AWS Config", "Amazon S3", "Auto Scaling Group", "VPC"],
            "answer": "Auto Scaling Group"
        }
    ]
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/student/login", methods=["GET", "POST"])
def student_login():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]

        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO students(name, email) VALUES(%s, %s)",
            (username, email)
        )

        connection.commit()

        return redirect(url_for("dashboard", username=username))

    return render_template("login.html")


@app.route("/student/dashboard/<username>")
def dashboard(username):

    return render_template(
        "dashboard.html",
        username=username,
        exam=exam
    )


@app.route("/exam/<username>", methods=["GET", "POST"])
def start_exam(username):

    if request.method == "POST":

        score = 0

        for i, q in enumerate(exam["questions"]):
            ans = request.form.get(f"q{i}")

            if ans == q["answer"]:
                score += 1

        cursor = connection.cursor()

        cursor.execute(
            "SELECT email FROM students WHERE name=%s ORDER BY id DESC LIMIT 1",
            (username,)
        )

        student = cursor.fetchone()

        cursor.execute(
            """
            INSERT INTO results(student, email, score, total, status)
            VALUES(%s, %s, %s, %s, %s)
            """,
            (
                username,
                student["email"],
                score,
                len(exam["questions"]),
                "PASS" if score >= 3 else "FAIL"
            )
        )

        connection.commit()

        return redirect(
            url_for(
                "result",
                username=username,
                score=score
            )
        )

    return render_template(
        "exam.html",
        username=username,
        exam=exam
    )


@app.route("/result/<username>/<int:score>")
def result(username, score):

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE name=%s ORDER BY id DESC LIMIT 1",
        (username,)
    )

    student = cursor.fetchone()

    return render_template(
        "result.html",
        student=student,
        score=score
    )


@app.route("/admin")
def admin():

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.execute("SELECT * FROM results")
    results = cursor.fetchall()

    return render_template(
        "admin.html",
        students=students,
        results=results
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
