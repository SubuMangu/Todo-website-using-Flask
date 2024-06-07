# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask,render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import desc
# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Todo(db.Model):
    slno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=True)
    desc=db.Column(db.String(500),nullable=True)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.slno} - {self.title}"
# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/',methods=['GET','POST'])
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    if request.method=='POST':
        title =request.form['title']
        desc=request.form['desc']
        todo=Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo=Todo.query.all()
    return render_template('design.html',allTodo=allTodo)
@app.route('/delete/<int:slno>')
def delete(slno):
    todo=Todo.query.filter_by(slno=slno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')
@app.route('/update/<int:slno>',methods=['GET','POST'])
def update(slno):
    if request.method=='POST':
        title =request.form['title']
        desc=request.form['desc']
        todo=Todo.query.filter_by(slno=slno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo=Todo.query.filter_by(slno=slno).first()
    return render_template('update.html',todo=todo)
# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug=True)
