from flask import Blueprint, jsonify, abort, make_response, request, flash, redirect, url_for, render_template
from app.models.task import Task
from app import db
from datetime import datetime
import requests
import os
from app import menu


tasks_bp = Blueprint("tasks_bp", __name__,  url_prefix="/tasks")
path="https://slack.com/api/chat.postMessage"
SLACK_API_KEY = 'xoxb-3491140412451-3484617014006-O1unyvDw54ykyZ7SIC4zsLEr'


def validate_task(id):
    try:
        id = int(id)
    except:
        
        abort(make_response({"message":f"task {id} invalid"}, 400))
    task = Task.query.get(id)

    if not task:

        abort(make_response({"message":f"task {id} not found"}, 404))
    return task


@tasks_bp.route("/post", methods=["POST", "GET"])
def create_task():
    if request.method == "POST":
        try:
            new_task = Task(title=request.form["title"],
                        description=request.form["description"])
        except KeyError:
            return {"details": "Invalid data"}, 400
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('about'))
    return  render_template('my-form.html', menu=menu)


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.order_by(Task.task_id.asc())
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict()["task"])
    return render_template( 'get_all_tasks.html', tasks=tasks_response, menu=menu)


@tasks_bp.route("/complete/", methods=["POST", "GET"])
def update_task1():
    if request.method == "POST":

        id=request.form['t_id']
        task = validate_task(id)
        mark=request.form['complete']

        if mark =="mark_complete":
            task.completed_at =datetime.utcnow() 
            slack_headers =  {"Authorization" : "Bearer "+SLACK_API_KEY}
            myobj={"channel" :"task-notifications",
                "text":f"Someone just completed the task {task.title}"}
            requests.post(path,data = myobj, headers=slack_headers)
            flash('Hurray!! You completed your task!!')

        elif mark =="mark_incomplete": 
            task.completed_at =None
            flash('Don\'t be upset, you will complete it later for sure')

        db.session.commit()
        # return redirect(url_for('about'))
   
    return  render_template('complete-form.html', title="Enter the id of your task and don't forget to check the box below", menu=menu)


@tasks_bp.route("/delete", methods=["POST"])
def delete_task():
    id=request.form['task_id']
    task = validate_task(id)
    db.session.delete(task)
    db.session.commit()

    return render_template('delete_one_task.html', task=task,title="One requested by id task was deleted", menu=menu)

@tasks_bp.route("/task_id", methods=["POST"])
def read_id():
    id=request.form['task_id']
    task = validate_task(id)
    return render_template('get_one_task.html', task=task,title="One requested by id task", menu=menu)

@tasks_bp.route("/<task_id>", methods=[ "GET"])
def read_one_task(task_id):
    return   render_template('id-form.html')
   

@tasks_bp.route("/update", methods=["POST", "GET"])
def update_task():
    if request.method == "POST":

        id=request.form['id']
        task = validate_task(id)
            
        task.title =request.form["title"]
        task.description = request.form["description"]

        db.session.commit()
        return redirect(url_for('about'))
   
    return  render_template('form-update.html', title="Update this task", menu=menu)