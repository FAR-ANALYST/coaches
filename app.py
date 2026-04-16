import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
# Secure key for session management
app.secret_key = "chess_uganda_2026_final_secure"

# --- FILE CONFIGURATION ---
# Using os.path.join ensures it works on both Windows and Render's Linux servers
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# This version prevents the 'FileExistsError' you saw in your logs
try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
except Exception as e:
    print(f"Note: Upload folder already exists or could not be created: {e}")

# --- GLOBAL DATA STORE ---
site_data = {
    "coach": {
        "name": "Kagulire Farouk",
        "photo": None,
        "location": "Kampala",
        "titles": "Candidate Master",
        "pricing": "50,000 UGX/hr",
        "bio": "Expert in technical strategies and data-driven chess analysis.",
        "expertise": ["Tactics", "Opening Theory", "Endgames"]
    },
    "live_game_url": "https://lichess.org/tv/frame?theme=brown&bg=dark"
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

# --- ROUTES ---

@app.route('/')
def index():
    """Lichess-style Public Index Page"""
    return render_template('index.html', coach=site_data['coach'], game_url=site_data['live_game_url'])

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    """Chessboard-themed Admin Dashboard"""
    global site_data
    if request.method == 'POST':
        # Update Coach Info
        site_data['coach'].update({
            "name": request.form.get('name'),
            "location": request.form.get('location'),
            "pricing": request.form.get('pricing'),
            "titles": request.form.get('titles'),
            "bio": request.form.get('bio'),
            "expertise": request.form.getlist('expertise_tags')
        })
        
        # Update Live Game URL
        site_data['live_game_url'] = request.form.get('live_game_url')

        # Handle Photo Upload
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                site_data['coach']['photo'] = filename

        flash("Platform updated successfully!", "success")
        return redirect(url_for('admin'))

    return render_template('admin.html', coach=site_data['coach'], game_url=site_data['live_game_url'])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
