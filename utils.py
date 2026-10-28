# utils.py — Reusable scenario calculation for TIMELOOP


def compute_scenarios(habits, duration_days):
    """Calculate baseline, improved, and reduced learning scenarios.

    Args:
        habits (dict): Keys 'study', 'sleep', 'social', 'skill' (hours/day).
        duration_days (int): Simulation length in days (30–180).

    Returns:
        dict with 'scenarios' and 'chart' data.
    """
    duration_days = max(30, min(180, int(duration_days)))

    skill = max(0.0, min(24.0, float(habits.get('skill', 0))))
    social = max(0.0, min(24.0, float(habits.get('social', 0))))

    baseline_daily = skill
    # Improved: move up to 30 min from social media, but not more than available
    improved_daily = baseline_daily + min(0.5, social)
    # Reduced: lose 30 min, never below zero
    reduced_daily = max(0.0, baseline_daily - 0.5)

    scenarios = {
        'baseline': {
            'name': 'Baseline',
            'daily': round(baseline_daily, 2),
            'hours': round(baseline_daily * duration_days, 1),
            'diff': 0,
            'description': 'Continue your current daily learning routine unchanged.',
            'color': '#0066cc',
        },
        'improved': {
            'name': 'Improved',
            'daily': round(improved_daily, 2),
            'hours': round(improved_daily * duration_days, 1),
            'diff': round((improved_daily - baseline_daily) * duration_days, 1),
            'description': 'Reallocate up to 30 minutes per day from social media to skill learning.',
            'color': '#00b894',
        },
        'reduced': {
            'name': 'Reduced',
            'daily': round(reduced_daily, 2),
            'hours': round(reduced_daily * duration_days, 1),
            'diff': round((reduced_daily - baseline_daily) * duration_days, 1),
            'description': 'Decrease skill-learning time by 30 minutes per day.',
            'color': '#e17055',
        },
    }

    # Chart series – cumulative hours at regular intervals
    num_points = 7
    step = max(1, duration_days // (num_points - 1))
    labels = list(range(0, duration_days + 1, step))
    if labels[-1] != duration_days:
        labels.append(duration_days)

    chart = {
        'labels': labels,
        'baseline': [round(baseline_daily * d, 1) for d in labels],
        'improved': [round(improved_daily * d, 1) for d in labels],
        'reduced': [round(reduced_daily * d, 1) for d in labels],
    }

    return {'scenarios': scenarios, 'chart': chart}
