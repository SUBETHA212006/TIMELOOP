# app.py — Flask backend for TIMELOOP
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from utils import compute_scenarios

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'timeloop-secret-key-change-in-production'


# ── Screen 1: Welcome / Landing ──────────────────────────────────────────
@app.route('/')
def welcome():
    return render_template('welcome.html')


# ── Screen 2: Profile Setup ──────────────────────────────────────────────
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        goal = request.form.get('goal', '')
        duration = request.form.get('duration', '180')
        errors = []
        if not name:
            errors.append('Please enter your name or nickname.')
        if not goal:
            errors.append('Please select a primary goal.')
        try:
            duration = int(duration)
            if duration < 30 or duration > 180:
                errors.append('Duration must be between 30 and 180 days.')
        except ValueError:
            errors.append('Duration must be a number.')
            duration = 180
        if errors:
            return render_template('profile.html', errors=errors,
                                   name=name, goal=goal, duration=duration)
        session['name'] = name
        session['goal'] = goal
        session['duration'] = duration
        return redirect(url_for('habits'))
    return render_template('profile.html', name=session.get('name', ''),
                           goal=session.get('goal', ''),
                           duration=session.get('duration', 180), errors=[])


# ── Screen 3: Daily Habit Input ──────────────────────────────────────────
@app.route('/habits', methods=['GET', 'POST'])
def habits():
    if not session.get('name'):
        return redirect(url_for('profile'))
    defaults = session.get('habits', {'study': 3, 'sleep': 8, 'social': 2, 'skill': 1.5})
    if request.method == 'POST':
        errors = []
        habit_data = {}
        for key in ('study', 'sleep', 'social', 'skill'):
            try:
                val = float(request.form.get(key, 0))
                if val < 0 or val > 24:
                    errors.append(f'{key.capitalize()} must be between 0 and 24.')
                habit_data[key] = round(val, 1)
            except ValueError:
                errors.append(f'{key.capitalize()} must be a valid number.')
                habit_data[key] = 0
        total = sum(habit_data.values())
        if total > 24:
            errors.append(f'Total hours ({total}) exceed 24. Please adjust.')
        if errors:
            return render_template('habits.html', habits=habit_data, errors=errors)
        session['habits'] = habit_data
        return redirect(url_for('analysis'))
    return render_template('habits.html', habits=defaults, errors=[])


# ── Screen 4: Habit Analysis ─────────────────────────────────────────────
@app.route('/analysis')
def analysis():
    habits = session.get('habits')
    if not habits:
        return redirect(url_for('habits'))
    duration = session.get('duration', 180)
    total = round(sum(habits.values()), 1)
    unallocated = round(24 - total, 1)
    result = compute_scenarios(habits, duration)
    return render_template('analysis.html', habits=habits, duration=duration,
                           total=total, unallocated=unallocated,
                           scenarios=result['scenarios'], chart=result['chart'])


# ── Screen 5: Simulation Dashboard ───────────────────────────────────────
@app.route('/dashboard')
def dashboard():
    habits = session.get('habits')
    if not habits:
        return redirect(url_for('habits'))
    duration = session.get('duration', 180)
    result = compute_scenarios(habits, duration)
    return render_template('dashboard.html', habits=habits, duration=duration,
                           scenarios=result['scenarios'], chart=result['chart'],
                           name=session.get('name', 'User'))


# ── Screen 6: Scenario Comparison ────────────────────────────────────────
@app.route('/comparison')
def comparison():
    habits = session.get('habits')
    if not habits:
        return redirect(url_for('habits'))
    duration = session.get('duration', 180)
    result = compute_scenarios(habits, duration)
    return render_template('comparison.html', habits=habits, duration=duration,
                           scenarios=result['scenarios'], chart=result['chart'])


# ── Screen 7: Future Timeline ────────────────────────────────────────────
@app.route('/timeline')
def timeline():
    habits = session.get('habits')
    if not habits:
        return redirect(url_for('habits'))
    duration = session.get('duration', 180)
    result = compute_scenarios(habits, duration)
    milestones = []
    for day in [30, 60, 90, 120, 150, 180]:
        if day <= duration:
            milestones.append({
                'day': day,
                'baseline': round(result['scenarios']['baseline']['daily'] * day, 1),
                'improved': round(result['scenarios']['improved']['daily'] * day, 1),
                'reduced': round(result['scenarios']['reduced']['daily'] * day, 1),
            })
    return render_template('timeline.html', habits=habits, duration=duration,
                           scenarios=result['scenarios'], chart=result['chart'],
                           milestones=milestones)


# ── Screen 8: Summary & Action Plan ──────────────────────────────────────
@app.route('/summary')
def summary():
    habits = session.get('habits')
    if not habits:
        return redirect(url_for('habits'))
    duration = session.get('duration', 180)
    scenario_key = request.args.get('scenario', 'baseline')
    result = compute_scenarios(habits, duration)
    scenarios = result['scenarios']
    selected = scenarios.get(scenario_key, scenarios['baseline'])
    goal = session.get('goal', 'skill learning')
    name = session.get('name', 'User')
    return render_template('summary.html', habits=habits, duration=duration,
                           scenarios=scenarios, selected=selected,
                           selected_key=scenario_key, goal=goal, name=name)


# ── API Endpoint ─────────────────────────────────────────────────────────
@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON payload provided'}), 400
    try:
        habits = data['habits']
        duration = int(data['duration'])
        duration = max(30, min(180, duration))
    except (KeyError, ValueError, TypeError) as e:
        return jsonify({'error': f'Invalid payload: {e}'}), 400
    result = compute_scenarios(habits, duration)
    return jsonify(result)


# ── Update duration via API ───────────────────────────────────────────────
@app.route('/api/set-duration', methods=['POST'])
def set_duration():
    data = request.get_json()
    try:
        duration = int(data['duration'])
        duration = max(30, min(180, duration))
        session['duration'] = duration
        return jsonify({'status': 'ok', 'duration': duration})
    except (KeyError, ValueError, TypeError):
        return jsonify({'error': 'Invalid duration'}), 400


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
