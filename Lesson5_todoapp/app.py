from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://udacitystudios@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)

# """
# # first try without database
# """

# @app.route('/')
# def index():
#     data_todo = [
#         {'description': 'Todo 1'},
#         {'description': 'Todo 2'},
#         {'description': 'Todo 3'}
#     ]
#     return render_template('index.html', data = data_todo)

"""
# second try with database
"""

@app.route('/v1')
def index1():
    data_todo = Todo.query.all()
    return render_template('index.html', data = data_todo)

@app.route('/v1/todos/create', method=['POST'])
def create_todo():
  description = request.form.get('description', '')
  todo = Todo(description=description)
  db.session.add(todo)
  db.session.commit()
  return redirect(url_for('index1'))

