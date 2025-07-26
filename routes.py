from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from extensions import db, login_manager
from flask_login import login_user, login_required, logout_user, current_user
from models import User, ExerciseLog, CalorieLog, WaterLog, BodyMeasurement, Goal, WorkoutPlan
from forms import LoginForm, RegisterForm, ExerciseForm, CalorieForm, WaterForm, MeasurementForm, GoalForm, PlanForm
import json
from datetime import date

bp = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(uid): return User.query.get(int(uid))


@bp.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))

@bp.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        u = User(username=form.username.data, email=form.email.data)
        u.set_password(form.password.data)
        db.session.add(u); db.session.commit()
        flash('Registered! Please log in.')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@bp.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()
        if u and u.check_password(form.password.data):
            login_user(u)
            return redirect(url_for('main.dashboard'))
        flash('Invalid credentials.')
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@bp.route('/dashboard')
@login_required
def dashboard():
    ex = ExerciseLog.query.filter_by(user=current_user).all()
    cal = CalorieLog.query.filter_by(user=current_user).all()
    wat = WaterLog.query.filter_by(user=current_user).all()
    meas = BodyMeasurement.query.filter_by(user=current_user).all()
    goals = Goal.query.filter_by(user=current_user).all()
    plans = WorkoutPlan.query.filter_by(user=current_user).all()
    return render_template('dashboard.html', exercises=ex, calories=cal, water=wat, measurements=meas, goals=goals, plans=plans)

@bp.route('/log_exercise', methods=['GET','POST'])
@login_required
def log_exercise():
    form = ExerciseForm()
    if form.validate_on_submit():
        e = ExerciseLog(user=current_user, name=form.name.data, reps=form.reps.data or 0, weight=form.weight.data or 0,
                        duration=form.duration.data or 0, calories=form.calories.data or 0, video_url=form.video_url.data)
        db.session.add(e); db.session.commit()
        flash('Exercise logged.')
        return redirect(url_for('main.dashboard'))
    return render_template('log_exercise.html', form=form)

@bp.route('/log_calories', methods=['GET','POST'])
@login_required
def log_calories():
    form = CalorieForm()
    if form.validate_on_submit():
        c = CalorieLog(user=current_user, calories=form.calories.data)
        db.session.add(c); db.session.commit()
        flash('Calories logged.')
        return redirect(url_for('main.dashboard'))
    return render_template('log_calories.html', form=form)

@bp.route('/log_water', methods=['GET','POST'])
@login_required
def log_water():
    form = WaterForm()
    if form.validate_on_submit():
        w = WaterLog(user=current_user, amount_ml=form.amount_ml.data)
        db.session.add(w); db.session.commit()
        flash('Water intake logged.')
        return redirect(url_for('main.dashboard'))
    return render_template('log_water.html', form=form)

@bp.route('/goals', methods=['GET','POST'])
@login_required
def goals():
    form = GoalForm()
    if form.validate_on_submit():
        g = Goal(user=current_user, description=form.description.data, target_date=form.target_date.data)
        db.session.add(g); db.session.commit()
        flash('Goal set.')
        return redirect(url_for('main.dashboard'))
    return render_template('goals.html', form=form, goals=Goal.query.filter_by(user=current_user).all())

@bp.route('/plan', methods=['GET','POST'])
@login_required
def plan():
    form = PlanForm()
    if form.validate_on_submit():
        p = WorkoutPlan(user=current_user, title=form.title.data, schedule=form.schedule.data)
        db.session.add(p); db.session.commit()
        flash('Workout Plan saved.')
        return redirect(url_for('main.dashboard'))
    return render_template('workout_plan.html', form=form, plans=WorkoutPlan.query.filter_by(user=current_user).all())

@bp.route('/progress')
def progress():
    calorie_labels = ['2025-07-01', '2025-07-02']
    calorie_values = [1800, 1950]
    weight_labels = ['2025-07-01', '2025-07-02']
    weight_values = [70.5, 70.2]

    return render_template(
        'progress.html',
        calorie_labels=calorie_labels,
        calorie_values=calorie_values,
        weight_labels=weight_labels,
        weight_values=weight_values
    )
