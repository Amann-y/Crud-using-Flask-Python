from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.Sno} {self.title}"

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form.get("title")
        desc = request.form.get("desc")
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html',allTodo=allTodo)

@app.route('/update/<int:Sno>',methods=['GET', 'POST'])
def update(Sno):
    if request.method == 'POST':
        upd_title = request.form.get("title")
        upd_desc = request.form.get("desc")
        todo = Todo.query.filter_by(Sno=Sno).first()
        todo.title= upd_title
        todo.desc = upd_desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(Sno=Sno).first()
    return render_template('update.html',todo=todo)

@app.route('/delete/<int:Sno>')
def delete(Sno):
    id = Todo.query.filter_by(Sno=Sno).first()
    db.session.delete(id)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)