from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys    

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:deemarco159@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)

db.create_all()

"""
# first try without database
"""

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

@app.route('/')
def index():
    data_todo = Todo.query.all()
    return render_template('index_sync.html', data = data_todo)

@app.route('/todos/create', methods=['POST'])
def create_todo():
  description = request.form.get('description', '')
  # description = request.get_json()['description']
  todo = Todo(description=description)
  db.session.add(todo)
  db.session.commit()
  return redirect(url_for('index'))

@app.route('/ajax')
def index2():
    data_todo = Todo.query.all()
    return render_template('index.html', data = data_todo)

@app.route('/ajax/todos/create', methods=['POST'])
def create_todo2():
  error = False
  body = {}
  print('hello')
  try:
    description = request.get_json()['description']
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    body['description'] = todo.description
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    print('erroor')
    abort (400)
  else:
    return jsonify(body)


