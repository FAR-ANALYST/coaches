import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "chess_uganda_2026_secure_key"

# --- CONFIGURATION ---
# Use a folder that Render can write to. 
# Note: On Render's free tier, these files will disappear when the server restarts 
# unless you connect a Persistent Disk or use external storage like Cloudinary.
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'pgn'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# --- DYNAMIC DATA STORE ---
# Initializing with empty strings so coaches can define themselves entirely.
coach_profile = {
    "name": "",
    "photo": None,  # Will store the filename after upload
    "location": "",
    "contact": "",
    "titles": "",
    "experience": "",
    "expertise": [],
    "pricing": "",
    "bio": ""
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- ROUTES ---

@app.route('/')
def index():
    # This would typically be the public-facing landing page for students.
    # For now, we redirect to the admin to let you set it up.
    return redirect(url_for('admin_dashboard'))

@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    global coach_profile
    
    if request.method == 'POST':
        # 1. Update text-based information
        coach_profile['name'] = request.form.get('name', '')
        coach_profile['location'] = request.form.get('location', '')
        coach_profile['contact'] = request.form.get('contact', '')
        coach_profile['titles'] = request.form.get('titles', '')
        coach_profile['experience'] = request.form.get('experience', '')
        coach_profile['pricing'] = request.form.get('pricing', '')
        coach_profile['bio'] = request.form.get('bio', '')
        
        # 2. Update multi-select expertise (list of checkboxes)
        coach_profile['expertise'] = request.form.getlist('expertise_tags')

        # 3. Handle Profile Photo Upload
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                coach_profile['photo'] = filename
        
        # 4. Handle Material Upload (Puzzles/Books)
        if 'material' in request.files:
            material_file = request.files['material']
            if material_file and material_file.filename != '' and allowed_file(material_file.filename):
                m_filename = secure_filename(material_file.filename)
                material_file.save(os.path.join(app.config['UPLOAD_FOLDER'], m_filename))
                # In a real app, you'd add this filename to a list of resources

        flash("Profile and pricing successfully updated!", "success")
        return redirect(url_for('admin_dashboard'))

    return render_template('admin.html', coach=coach_profile)

if __name__ == '__main__':
    # On Render, the port is usually 10000, but Flask defaults to 5000.
    # Using '0.0.0.0' allows it to be accessed externally.
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
