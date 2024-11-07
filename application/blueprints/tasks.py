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
        flash("Oppgaven ble ikke funnet", "error")
        return redirect(url_for('tasks.show_page'))
    
    # Toggler 'scheduled'-status
    task.scheduled = not task.scheduled
    db.session.commit()
    flash(f"Oppgave '{task.name}' sin status ble endret.", "success")
    return redirect(url_for('tasks.show_page'))

@tasks.route('/tasks/<int:task_id>/set_time', methods=['POST'])
def set_time(task_id):
    """Setter tiden for en oppgave."""
    task = Task.query.get(task_id)
    if not task:
        flash("Oppgaven ble ikke funnet", "error")
        return redirect(url_for('tasks.show_page'))
    
    # Setter tid for oppgaven
    task.time = request.form.get('time')
    db.session.commit()
    flash(f"Tidspunkt for oppgave '{task.name}' ble oppdatert.", "success")
    return redirect(url_for('tasks.show_page'))
