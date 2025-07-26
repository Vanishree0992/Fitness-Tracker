from flask import Flask, request, jsonify
from extensions import db, login_manager
from models import User, ExerciseLog
from flask_login import login_required, current_user

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(uid): return User.query.get(int(uid))

@app.route('/api/exercises', methods=['GET','POST'])
@login_required
def api_exercises():
    if request.method == 'POST':
        data = request.json
        e = ExerciseLog(user=current_user, **data)
        db.session.add(e); db.session.commit()
        return jsonify({'status':'ok'})
    logs = ExerciseLog.query.filter_by(user=current_user).all()
    return jsonify([{'name':e.name,'reps':e.reps,'weight':e.weight,'timestamp':e.timestamp.isoformat()} for e in logs])
