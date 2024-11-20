# Taskrute med funksjoner for å vise og endre oppgaver

from flask import Blueprint, render_template, request, redirect, url_for, flash
from adapters.database.task_flask import Task
from core.utils import is_valid_time

tasks = Blueprint('tasks', __name__)

# Viser oppgavesiden med alle oppgaver
@tasks.route('/tasks')
def show_page():
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

# Viser kontrollpanelet for en oppgave, og håndterer endring av tid og på/av-scheduling
@tasks.route('/tasks/<int:task_id>', methods=['GET', 'POST'])
def task_detail(task_id):
    task = Task.get_by_id(Task, task_id)
    if not task:
        return redirect(url_for('tasks.show_page'))

    if request.method == 'POST':
        if 'toggle_schedule' in request.form:
            task.set('scheduled', not task.get('scheduled'))
            flash(f"{'Aktivert' if task.get('scheduled') else 'Deaktivert'}", 'message')
        
        elif 'set_time' in request.form:
            time = request.form.get('time')
            if not is_valid_time(time):
                flash('Ugyldig tid', 'error')
            else:
                task.set('time', time)
                flash('Tid endret', 'success')
        
        task.save()

        return redirect(url_for('tasks.task_detail', task_id=task_id))

    return render_template('task_detail.html', task=task)
