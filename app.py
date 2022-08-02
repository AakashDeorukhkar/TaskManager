from crypt import methods
from importlib.resources import contents
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column
from datetime import datetime

app = Flask(__name__)   #Referencing this file
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/TaskManager' #Config tells us where the db is located

db = SQLAlchemy(app)

class ToDo(db.Model):   #Creating the database Schemas
    __tablename__ = "TaskManager"
    id = Column(db.Integer,primary_key=True)
    content = Column(db.String(200),nullable=False)
    date_created = Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return "<Task %r>" %self.id


@app.route('/', methods=['POST','GET'])    # Routing our app
def index():    #Defining a method for the route
    if request.method == "POST":
        task_content = request.form['content']  #Get 'content' from Form Action in HTML
        
        new_task = ToDo(content=task_content)   #Setting content in DB to task_content

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        
        except:
            return "There was an issue adding your task"

    else: #If action is not "POST"
        tasks = ToDo.query.order_by(ToDo.date_created).all()    #Fetch all tasks and order them by Date Created
        return render_template('index.html',tasks=tasks)    

@app.route('/delete/<int:id>')  #Deleting a task with reference to Primary Key
def delete(id):
    task_to_delete = ToDo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    
    except:
        return "Something went wrong while trying to delete your task"
    
@app.route('/update/<int:id>', methods=['GET','POST'])  #Updating a task with reference to Primary Key
def update(id):
    task = ToDo.query.get_or_404(id)

    if request.method == "POST":
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')

        except:
            return "There was an error updating your task"


    else:
        return render_template('update.html',task=task)  #Rendering "update.html" for the selected task


if __name__=='__main__':
    app.run(debug=True)


