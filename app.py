import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
# A unique secret key for your Uganda-based session management
app.secret_key = "chess_uganda_final_2026_secure_key"

# --- FILE CONFIGURATION ---
# Using os.path.join ensures compatibility between local Windows and Render's Linux environment
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# The 'exist_ok=True' parameter prevents the crash you experienced if the folder already exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- GLOBAL DATA STORE ---
# Initializing with your profile details while keeping it flexible for updates
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
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# --- ROUTES ---

@app.route('/')
def index():
    """Public Lichess-style Index Page."""
    return render_template('index.html', coach=site_data['coach'], game_url=site_data['live_game_url'])

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    """Chessboard-themed Admin Dashboard."""
    global site_data
    if request.method == 'POST':
        # Update Coach Information from the form
        site_data['coach'].update({
            "name": request.form.get('name'),
            "location": request.form.get('location'),
            "pricing": request.form.get('pricing'),
            "titles": request.form.get('titles'),
            "bio": request.form.get('bio'),
            "expertise": request.form.getlist('expertise_tags')
        })
        
        # Update the Live Game URL (updated from admin to reflect on index)
        site_data['live_game_url'] = request.form.get('live_game_url')

        # Handle Profile Photo Upload
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                site_data['coach']['photo'] = filename

        flash("Platform settings updated successfully!", "success")
        return redirect(url_for('admin'))

    return render_template('admin.html', coach=site_data['coach'], game_url=site_data['live_game_url'])

if __name__ == '__main__':
    # Render provides a 'PORT' environment variable; default to 5000 for local testing
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
