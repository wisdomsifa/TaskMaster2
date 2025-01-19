from flask import render_template, url_for, redirect, flash, request
from taskmaster import app, db,  bcrypt
from taskmaster.form import RegistrationForm, LoginForm, TaskForm
from taskmaster.models import User, Task
from flask_login import login_user, current_user, logout_user, login_required
import secrets, os

@app.route("/home")
@login_required
def home():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('home.html', tasks=tasks)

# @app.route("/search", methods=['GET'])
# @login_required
# def search():
#     query = request.args.get('query', '').strip()
#     if query:
#         first_letter = query[0].lower()
#         results = Student.query.filter(Student.studentname.ilike(f'{first_letter}%')).all()
#     else:
#         results = []
#     return render_template('search.html', results=results)

@app.route("/task", methods=['GET', 'POST'])
@login_required
def task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data, 
            user_id=current_user.id, 
            description=form.description.data,
            creator=form.creator.data, 

        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('task.html', title ='task', form=form)

# @app.route("/home/<int:task_id>")
# @login_required
# def beneficiary(task_id):
#     created_task = Student.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
#     return render_template('created_task.html', title=created_task.title, created_task=created_task)


@app.route("/register", methods=['GET', 'POST']) 
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for username { form.username.data } successfully, you are now able to login!", 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title='register', form=form)


@app.route("/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash(f"Your are logged in as { form.username.data }", 'success')
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash(f'Incorrect username or password', 'danger')
    return render_template("login.html", title='login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

# @app.route("/description")
# @login_required
# def description():
#     tasks = Task.query.filter_by(user_id=current_user.id).all()
#     return render_template('description.html', tasks=tasks)


# @app.route("/home/<int:task_id>/delete")
# @login_required
# def delete_task(task_id):
#     created_task = Student.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
#     db.session.delete(created_task)
#     db.session.commit()
#     flash(f'Task {created_task.title} successfullly deleted', 'success')
#     return redirect(url_for('home'))
@app.route("/contact")
@login_required
def contact():
    return render_template('contact.html')


@app.route("/dashboard")
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', tasks=tasks)


@app.route("/notifications")
@login_required
def notifications():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('notifications.html', tasks=tasks)

@app.route("/profile")
@login_required
def profile():
    return render_template('profile.html')

@app.route("/calendar")
@login_required
def calendar():
    return render_template('calendar.html')
