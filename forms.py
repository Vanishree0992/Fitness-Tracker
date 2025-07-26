from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, IntegerField, TextAreaField, DateField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(LoginForm):
    username = StringField('Username', validators=[DataRequired()])
    
class ExerciseForm(FlaskForm):
    name = StringField('Exercise', validators=[DataRequired()])
    reps = IntegerField('Reps')
    weight = FloatField('Weight (kg)')
    duration = FloatField('Duration (min)')
    calories = FloatField('Calories Burned')
    video_url = StringField('Video URL')
    submit = SubmitField('Log Exercise')

class CalorieForm(FlaskForm):
    calories = FloatField('Calories', validators=[DataRequired()])
    submit = SubmitField('Log Calories')

class WaterForm(FlaskForm):
    amount_ml = IntegerField('Water (ml)', validators=[DataRequired()])
    submit = SubmitField('Log Water')

class MeasurementForm(FlaskForm):
    weight = FloatField('Weight (kg)')
    body_fat = FloatField('Body Fat %')
    submit = SubmitField('Save')
    
class GoalForm(FlaskForm):
    description = StringField('Goal', validators=[DataRequired()])
    target_date = DateField('Target Date', validators=[DataRequired()])
    submit = SubmitField('Set Goal')

class PlanForm(FlaskForm):
    title = StringField('Plan Title', validators=[DataRequired()])
    schedule = TextAreaField('Schedule (JSON)', validators=[DataRequired()])
    submit = SubmitField('Save Plan')
