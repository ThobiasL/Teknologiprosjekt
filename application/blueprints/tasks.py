from flask import Blueprint, render_template, request, redirect, url_for, flash
from core.models.task import Task
from adapters.database import db

tasks = Blueprint('tasks', __name__)

@tasks.route('/tasks')
def show_page():
    """Viser oppgavesiden med alle oppgaver."""
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

@tasks.route('/tasks/<int:task_id>/toggle_schedule', methods=['POST'])
def toggle_schedule(task_id):
    """Toggler 'scheduled'-status for en oppgave."""
    task = Task.query.get(task_id)
    if not task:
        return redirect(url_for('tasks.show_page'))
    
    task.scheduled = not task.scheduled
    db.session.commit()
    return redirect(url_for('tasks.task_detail', task_id=task_id))

@tasks.route('/tasks/<int:task_id>/set_time', methods=['POST'])
def set_time(task_id):
    """Setter tiden for en oppgave."""
    task = Task.query.get(task_id)
    if not task:
        return redirect(url_for('tasks.show_page'))
    
    task.time = request.form.get('time')
    db.session.commit()
    return redirect(url_for('tasks.task_detail', task_id=task_id))

@tasks.route('/tasks/<int:task_id>', methods=['GET', 'POST'])
def task_detail(task_id):
    task = Task.query.get(task_id)
    if not task:
        return redirect(url_for('tasks.show_page'))
    
    return render_template('task_detail.html', task=task)
