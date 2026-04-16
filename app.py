import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "chess_uganda_2026_pro_key"

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'pgn'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Global data store (In production, use a Database like SQLite or PostgreSQL)
site_data = {
    "coach": {
        "name": "Kagulire Farouk",
        "photo": None,
        "location": "Kampala",
        "contact": "+256...",
        "titles": "Candidate Master",
        "experience": "5",
        "expertise": ["Tactics", "Opening Theory"],
        "pricing": "50,000 UGX/hr",
        "bio": "Professional coach based in Uganda."
    },
    "stream_url": "https://www.youtube.com/embed/live_stream?channel=UCexample" # Default placeholder
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html', coach=site_data['coach'], stream_url=site_data['stream_url'])

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    global site_data
    if request.method == 'POST':
        # Update Coach Info
        site_data['coach']['name'] = request.form.get('name')
        site_data['coach']['location'] = request.form.get('location')
        site_data['coach']['pricing'] = request.form.get('pricing')
        site_data['coach']['titles'] = request.form.get('titles')
        site_data['coach']['bio'] = request.form.get('bio')
        site_data['coach']['expertise'] = request.form.getlist('expertise_tags')
        
        # Update Stream URL (The Main Coach can change this for live events)
        new_stream = request.form.get('stream_url')
        if new_stream:
            site_data['stream_url'] = new_stream

        # Handle Photo
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                site_data['coach']['photo'] = filename

        flash("System Updated Successfully!", "success")
        return redirect(url_for('admin'))

    return render_template('admin.html', coach=site_data['coach'], stream_url=site_data['stream_url'])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
