from flask import Blueprint, render_template, request, redirect, url_for, flash
from adapters.database.task_db import Task
from core.utils import is_valid_time

tasks = Blueprint('tasks', __name__)

@tasks.route('/tasks')
def show_page():
    """Viser oppgavesiden med alle oppgaver."""
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

# Viser kontrollpanelet for en oppgave, og håndterer oppdateringer (toggle og set_time)
@tasks.route('/tasks/<int:task_id>', methods=['GET', 'POST'])
def task_detail(task_id):
    task = Task.get_by_id(Task, task_id)
    if not task:
        return redirect(url_for('tasks.show_page'))

    if request.method == 'POST':
        # Håndter toggling av schedule
        if 'toggle_schedule' in request.form:
            task.set('scheduled', not task.get('scheduled'))
            flash(f"{'Aktivert' if task.get('scheduled') else 'Deaktivert'}", 'message')
        
        # Håndter setting av tid
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
