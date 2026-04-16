import os
import random
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
# Secure key for session management and flash messages
app.secret_key = "chess_uganda_2026_final_secure_v3"

# --- FILE CONFIGURATION ---
# Using os.path.join ensures compatibility between local Windows and Render's Linux environment
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 'exist_ok=True' prevents the crash on Render if the folder already exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- GLOBAL DATA STORE ---
# Multi-coach support and live game monitoring
site_data = {
    "coaches": [
        {
            "name": "Kagulire Farouk",
            "photo": None,
            "location": "Kampala",
            "titles": "Candidate Master",
            "pricing": "50,000 UGX/hr",
            "bio": "Expert in technical strategies and data-driven chess analysis. Professional coach based in Uganda."
        },
        {
            "name": "Grace Nsubuga",
            "photo": None,
            "location": "Entebbe",
            "titles": "FIDE Master",
            "pricing": "70,000 UGX/hr",
            "bio": "National champion focused on middle-game mastery and tactical precision."
        }
    ],
    "live_game_url": "https://lichess.org/tv/frame?theme=brown&bg=dark" # Default live feed
}

def allowed_file(filename):
    """Check if the uploaded file has a valid extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# --- ROUTES ---

@app.route('/')
def index():
    """Public Lichess-style Index Page with player monitoring."""
    # Simulated live player counts for Ugandan time control pools
    stats = {
        "1+0": random.randint(20, 50),
        "2+1": random.randint(15, 40),
        "3+0": random.randint(40, 100),
        "3+2": random.randint(30, 80),
        "5+0": random.randint(15, 45),
        "5+5": random.randint(10, 35),
        "10+0": random.randint(50, 120),
        "15+10": random.randint(10, 30)
    }
    return render_template('index.html', coaches=site_data['coaches'], game_url=site_data['live_game_url'], stats=stats)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    """Chessboard-themed Admin Dashboard."""
    global site_data
    if request.method == 'POST':
        # Update the primary coach's details (index 0)
        site_data['coaches'][0].update({
            "name": request.form.get('name'),
            "location": request.form.get('location'),
            "pricing": request.form.get('pricing'),
            "titles": request.form.get('titles'),
            "bio": request.form.get('bio')
        })
        
        # Update the Live Game URL from the admin panel
        site_data['live_game_url'] = request.form.get('live_game_url')

        # Handle Profile Photo Upload
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                site_data['coaches'][0]['photo'] = filename

        flash("Platform settings and live feed updated!", "success")
        return redirect(url_for('admin'))

    # Passing the first coach to the admin template for editing
    return render_template('admin.html', coach=site_data['coaches'][0], game_url=site_data['live_game_url'])

if __name__ == '__main__':
    # Render provides a 'PORT' environment variable; default to 5000 for local testing
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
