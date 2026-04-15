from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "chess_uganda_2026_key"

# Configuration for uploads
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'pgn', 'jpg', 'png', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initial Mock Data (In a real app, this would come from a Database)
coach_profile = {
    "name": "Kagulire Farouk",
    "photo": "default_avatar.png",
    "location": "Kampala, Uganda",
    "contact": "+256 700 000000",
    "titles": "Candidate Master (CM)",
    "experience": 5,
    "expertise": ["Opening Theory", "Tactics"],
    "pricing": "50,000 UGX"
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # Redirecting to dashboard for now as requested for the Admin page
    return redirect(url_for('admin_dashboard'))

@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    global coach_profile
    
    if request.method == 'POST':
        # 1. Handle Profile Info
        coach_profile['name'] = request.form.get('name')
        coach_profile['location'] = request.form.get('location')
        coach_profile['contact'] = request.form.get('contact')
        coach_profile['titles'] = request.form.get('titles')
        coach_profile['experience'] = request.form.get('experience')
        coach_profile['pricing'] = request.form.get('pricing')
        
        # 2. Handle Multi-select Expertise
        selected_expertise = request.form.getlist('expertise_tags')
        coach_profile['expertise'] = selected_expertise

        # 3. Handle File/Photo Uploads
        if 'photo' in request.files:
            file = request.files['photo']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                coach_profile['photo'] = filename

        flash("Coach Profile Updated Successfully!", "success")
        return redirect(url_for('admin_dashboard'))

    return render_template('admin.html', coach=coach_profile)

if __name__ == '__main__':
    app.run(debug=True)
