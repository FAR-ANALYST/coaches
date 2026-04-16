import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "chess_uganda_ultra_key"

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global data store
site_data = {
    "coach": {
        "name": "",
        "photo": None,
        "location": "",
        "titles": "",
        "pricing": "",
        "bio": "",
        "expertise": []
    },
    "live_game_url": "https://lichess.org/tv/frame?theme=brown&bg=dark" # Default Lichess TV
}

@app.route('/')
def index():
    return render_template('index.html', coach=site_data['coach'], game_url=site_data['live_game_url'])

@app.route('/admin', methods=['GET', 'POST'])
def admin():
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
        
        # New Feature: Update Live Game URL
        site_data['live_game_url'] = request.form.get('live_game_url')

        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                site_data['coach']['photo'] = filename

        flash("Coach Profile & Live Game Updated!", "success")
        return redirect(url_for('admin'))

    return render_template('admin.html', coach=site_data['coach'], game_url=site_data['live_game_url'])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
