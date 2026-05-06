from flask import Flask , redirect,request,url_for,flash,session ,render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'se'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class Task(db.Model):

    id = db.Column(db.Integer , primary_key=True)
    content = db.Column(db.String(200) , nullable=False)

@app.route("/" , methods=['GET' , 'POST'])
def home():
    if request.method == "POST":
        task_content = request.form.get("task")

        if task_content:
            new_task = Task(content=task_content)
            db.session.add(new_task)
            db.session.commit()

        return redirect(url_for("home")) 

    tasks = Task.query.all()    
    return render_template("index.html" , tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()

    return redirect(url_for("home"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
