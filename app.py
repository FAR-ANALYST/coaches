import os
import random
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
# Secure key for session and flash messages
app.secret_key = "chess_uganda_2026_omni_v5"

# --- THE DEFINITIVE FIX FOR STATUS 1 ---
# This block prevents the 'FileExistsError' seen in your logs
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def ensure_upload_dir():
    """Handles folder creation safely to avoid Render's startup crash."""
    if not os.path.exists(UPLOAD_FOLDER):
        try:
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        except Exception as e:
            # Logs the status but allows the app to continue booting
            print(f"Startup Note: Upload directory check: {e}")

ensure_upload_dir()

# --- GLOBAL DATA STORE ---
site_data = {
    "coaches": [
        {
            "id": 1,
            "name": "Kagulire Farouk",
            "photo": None,
            "titles": "Candidate Master",
            "pricing": "50,000 UGX/hr",
            "bio": "Expert in technical strategies and data-driven chess analysis. Based in Kampala."
        },
        {
            "id": 2,
            "name": "Grace Nsubuga",
            "photo": None,
            "titles": "FIDE Master",
            "pricing": "70,000 UGX/hr",
            "bio": "National champion focused on middle-game mastery and tactical precision."
        }
    ],
    # MULTI-GAME SUPPORT
    "live_games": [
        {"title": "Main Arena (Lichess TV)", "url": "https://lichess.org/tv/frame?theme=brown&bg=dark"},
        {"title": "Uganda Top Board", "url": "https://lichess.org/tv/frame?theme=blue&bg=dark"},
        {"title": "Blitz Championship", "url": "https://lichess.org/tv/frame?theme=green&bg=dark"}
    ]
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# --- ROUTES ---

@app.route('/')
def index():
    """Lobby with categorized time formats and game dropdown."""
    # Simulated live counts for Ugandan pools
    stats = {
        "1+0": random.randint(20, 50), "2+1": random.randint(15, 40),
        "3+0": random.randint(40, 100), "3+2": random.randint(30, 80), 
        "5+0": random.randint(15, 45), "5+5": random.randint(10, 35), 
        "10+0": random.randint(50, 120), "15+10": random.randint(10, 30)
    }
    return render_template('index.html', 
                           coaches=site_data['coaches'], 
                           games=site_data['live_games'], 
                           stats=stats)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    """Admin portal to manage coach profile and primary game link."""
    global site_data
    if request.method == 'POST':
        # Update the first coach in the list
        site_data['coaches'][0].update({
            "name": request.form.get('name'),
            "pricing": request.form.get('pricing'),
            "titles": request.form.get('titles'),
            "bio": request.form.get('bio')
        })
        
        # Update the primary game URL
        site_data['live_games'][0]['url'] = request.form.get('live_game_url')

        # Handle Photo Upload
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                site_data['coaches'][0]['photo'] = filename

        flash("Platform settings updated successfully!", "success")
        return redirect(url_for('admin'))

    return render_template('admin.html', coach=site_data['coaches'][0], game_url=site_data['live_games'][0]['url'])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
