# TIMELOOP – Experience the Consequences of Your Habits

## Overview
TIMELOOP is a lightweight web application that lets users model how their daily habits affect the amount of time they can spend on skill‑learning over the next six months.  Users enter their routine, choose a simulation length, and see three scenarios:

* **Baseline** – keep the current learning time.
* **Improved** – re‑allocate up to 30 minutes from social media to learning.
* **Reduced** – lose up to 30 minutes of learning per day.

The app visualises the data with Chart.js and stores the inputs in the user’s session so they persist while navigating between the eight screens.

## Project Structure
```
TIMELOOP_Project/
├─ app.py                # Flask backend and routes
├─ utils.py              # Scenario calculation logic
├─ requirements.txt      # Python dependencies
├─ README.md             # This file
├─ static/
│   ├─ css/style.css     # Global styling
│   └─ img/illustration.svg  # Placeholder illustration (replace with your own)
└─ templates/
    ├─ base.html          # Base layout with navigation
    ├─ welcome.html       # Screen 1 – Landing page
    ├─ profile.html       # Screen 2 – Profile setup
    ├─ habits.html        # Screen 3 – Daily habit input
    ├─ analysis.html      # Screen 4 – Habit analysis
    ├─ dashboard.html     # Screen 5 – Simulation dashboard
    ├─ comparison.html    # Screen 6 – Scenario comparison
    ├─ timeline.html      # Screen 7 – Future timeline
    └─ summary.html       # Screen 8 – Summary & action plan
```

## Setup & Execution
1. **Install Python 3.9+** (if not already installed).
2. Open a terminal in `C:\Users\Lenovo\OneDrive\Desktop\TIMELOOP_Project`.
3. (Optional) Create a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
4. Install the required packages:
   ```powershell
   pip install -r requirements.txt
   ```
5. Run the Flask development server:
   ```powershell
   python app.py
   ```
   The app will be available at `http://127.0.0.1:5000/`.
6. Open the URL in a browser and walk through the eight screens.

## How It Works
* **Session storage** – Flask’s signed cookies keep the user’s name, goal, habit values and selected duration across requests.
* **`utils.compute_scenarios`** – a pure‑Python function that takes the habit dict and a duration (days) and returns:
  * the three scenario objects (`baseline`, `improved`, `reduced`)
  * cumulative learning hours for each scenario
  * chart data (labels + cumulative series) used by Chart.js.
* **Frontend** – Each screen is a Jinja template that pulls data from the session or from the `/api/calculate` endpoint.  Charts are rendered with Chart.js, and simple JavaScript keeps the total‑hours label and the dashboard slider in sync.

## Extending the Project
* Replace `static/img/illustration.svg` with a custom illustration.
* Add persistent storage (SQLite) if you wish to save simulations permanently.
* Refactor the JavaScript to avoid page reloads after the dashboard slider change – the current implementation works but can be made smoother.

## Disclaimer
The projections are **hypothetical** and do **not** guarantee any personal outcomes.  They are intended solely for exploratory, educational purposes.
