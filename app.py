from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

students = []
results = []

exam = {
    "title": "AWS Cloud Fundamentals",
    "questions": [
        {
            "question": "Which AWS service provides virtual servers?",
            "options": ["S3", "EC2", "Lambda", "RDS"],
            "answer": "EC2"
        },
        {
            "question": "Which service stores objects?",
            "options": ["EC2", "S3", "VPC", "IAM"],
            "answer": "S3"
        }
    ]
}

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/student/login", methods=["GET","POST"])
def student_login():

    if request.method=="POST":
        username=request.form["username"]
        students.append(username)
        return redirect(url_for("dashboard",username=username))

    return render_template("login.html")


@app.route("/student/dashboard/<username>")
def dashboard(username):
    return render_template("dashboard.html",
                           username=username,
                           exam=exam)


@app.route("/exam/<username>",methods=["GET","POST"])
def start_exam(username):

    if request.method=="POST":

        score=0

        for i,q in enumerate(exam["questions"]):
            ans=request.form.get(f"q{i}")

            if ans==q["answer"]:
                score+=1

        results.append({
            "student":username,
            "score":score
        })

        return redirect(url_for("result",
                                username=username,
                                score=score))

    return render_template("exam.html",
                           username=username,
                           exam=exam)


@app.route("/result/<username>/<int:score>")
def result(username,score):
    return render_template("result.html",
                           username=username,
                           score=score,
                           total=len(exam["questions"]))


@app.route("/admin")
def admin():

    return render_template("admin.html",
                           students=students,
                           results=results,
                           exam=exam)


if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
