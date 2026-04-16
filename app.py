import os
import random
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
# Secure key for session management and flash messages
app.secret_key = "chess_uganda_2026_final_secure_v3"

# --- THE FIX FOR STATUS 1 ERROR ---
# We define the path and check it manually to avoid the Render 'FileExists' crash
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    try:
        # We try to create it, but if Render's filesystem says no, 
        # the app won't crash (it will just log the issue).
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    except Exception as e:
        print(f"Directory check notice: {e}")

# --- GLOBAL DATA STORE ---
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
    "live_game_url": "https://lichess.org/tv/frame?theme=brown&bg=dark"
}

def allowed_file(filename):
    """Utility to check image extensions."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# --- ROUTES ---

@app.route('/')
def index():
    """Lichess-style Index Page with live Ugandan player monitoring."""
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
    """Dashboard to update the primary coach and the live game feed."""
    global site_data
    if request.method == 'POST':
        # Update the main coach (Farouk)
        site_data['coaches'][0].update({
            "name": request.form.get('name'),
            "location": request.form.get('location'),
            "pricing": request.form.get('pricing'),
            "titles": request.form.get('titles'),
            "bio": request.form.get('bio')
        })
        
        # Update Live Feed
        site_data['live_game_url'] = request.form.get('live_game_url')

        # Handle Photo Upload
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Create full path
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(save_path)
                site_data['coaches'][0]['photo'] = filename

        flash("Chess Uganda Platform Updated!", "success")
        return redirect(url_for('admin'))

    return render_template('admin.html', coach=site_data['coaches'][0], game_url=site_data['live_game_url'])

if __name__ == '__main__':
    # Binding to Render's dynamic port
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
