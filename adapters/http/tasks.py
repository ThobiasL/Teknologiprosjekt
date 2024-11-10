from flask import Blueprint, render_template, request, redirect, url_for, flash
from core.models.task import Task
from core.utils import is_valid_time

tasks = Blueprint('tasks', __name__)

@tasks.route('/tasks')
def show_page():
    """Viser oppgavesiden med alle oppgaver."""
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

# Viser kontrollpanelet for en oppgave
@tasks.route('/tasks/<int:task_id>', methods=['GET', 'POST'])
def task_detail(task_id):
    task = Task.get_by_id(Task, task_id)
    if not task:
        return redirect(url_for('tasks.show_page'))
    
    return render_template('task_detail.html', task=task)

# Toggler en oppgave på eller av
@tasks.route('/tasks/<int:task_id>/toggle_schedule', methods=['POST'])
def toggle_schedule(task_id):

    task = Task.get_by_id(Task, task_id)
    
    if not task:
        return redirect(url_for('tasks.show_page'))
    
    task.set('scheduled', not task.get('scheduled'))
    return redirect(url_for('tasks.task_detail', task_id=task_id))

# Setter tiden for en oppgave
@tasks.route('/tasks/<int:task_id>/set_time', methods=['POST'])
def set_time(task_id):
    task = Task.get_by_id(Task, task_id)
    time = request.form.get('time')

    if not is_valid_time(time):
        flash('Ugyldig tid', 'error')
        return redirect(url_for('tasks.task_detail', task_id=task_id))

    task.set('time', time)
    flash('Tid endret', 'message')
    return redirect(url_for('tasks.task_detail', task_id=task_id))


