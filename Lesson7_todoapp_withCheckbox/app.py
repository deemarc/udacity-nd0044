from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys    

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)
  completed = db.Column(db.Boolean, nullable=False, default=False)
  todolist_id = db.Column(db.Integer, db.ForeignKey('todo_lists.id', ondelete='cascade'), nullable=False)

class TodoList(db.Model):
  __tablename__ = 'todo_lists'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)
  todos = db.relationship('Todo', backref='todolist', lazy=True, cascade="save-update, merge, delete")

@app.route('/todolist/<todolist_id>')
def get_list_todos(todolist_id):
    todos = Todo.query.filter_by(todolist_id=todolist_id).order_by('id').all()
    todos_lists = TodoList.query.order_by('id').all()
    active_todolist = TodoList.query.filter_by(id=todolist_id).first()
    return render_template('index.html', todos = todos, active_todolist= active_todolist, todos_lists = todos_lists)

@app.route('/')
def index():
  return redirect(url_for('get_list_todos', todolist_id=1))

@app.route('/todolist/create', methods=['POST'])
def create_todoList():
  error = False
  body = {}
  try:
    name = request.get_json()['name']
    todo_list = TodoList(name=name)
    db.session.add(todo_list)
    db.session.commit()
    body['id'] = todo_list.id
    body['name'] = todo_list.name
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return jsonify(body)


@app.route('/todos/create', methods=['POST'])
def create_todo():
  error = False
  body = {}
  try:
    description = request.get_json()['description']
    todolistId = request.get_json()['todolist_id']
    if not TodoList.query.filter_by(id=todolistId).first():
      abort(404, 'Given todo list id cannot be found')
    
    todo = Todo(description=description,todolist_id=todolistId)
    
    db.session.add(todo)
    db.session.commit()
    body['id'] = todo.id
    body['completed'] = todo.completed
    body['description'] = todo.description
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort(400)
  else:
    return jsonify(body)

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_complete_todo(todo_id):
  error = False
  try:
    completed = request.get_json()['completed']
    todo = Todo.query.get(todo_id)
    todo.completed = completed
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return redirect(url_for('index'))

@app.route('/todolist/<todoList_id>', methods=['DELETE'])
def delete_todoList(todoList_id):
  error = False
  try:
    TodoList.query.filter_by(id=todoList_id).delete()
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return jsonify({ 'success': True })

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo_item(todo_id):
  error = False
  try:
    Todo.query.filter_by(id=todo_id).delete()
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return jsonify({ 'success': True })

