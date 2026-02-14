import os
import csv
from flask import Flask, render_template, request, redirect, send_from_directory

app = Flask(__name__)

# Ensure upload folders exist (will not error if they already exist)
os.makedirs('uploads/images', exist_ok=True)
os.makedirs('uploads/voices', exist_ok=True)

@app.route('/')
def portal():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "admin" and password == "admin123":
            return redirect('/admin')
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/admin')
def admin_dashboard():
    submissions = []
    if os.path.exists('submissions.csv'):
        with open('submissions.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                submissions.append(row)
    return render_template('dashboard.html', submissions=submissions)

@app.route('/uploads/<folder>/<filename>')
def uploaded_file(folder, filename):
    return send_from_directory(os.path.join('uploads', folder), filename)

@app.route('/submit', methods=['POST'])
def submit():
    print("Submit route accessed!")  # Debug: confirms route is triggered
    name = request.form.get('name')
    phone = request.form.get('phone')
    location = request.form.get('location')
    problem = request.form.get('problem')
    help_type = request.form.get('help_type')

    image = request.files.get('image')
    voice = request.files.get('voice')
    image_filename = ""
    voice_filename = ""

    if image and image.filename:
        image_filename = os.path.join('uploads/images', image.filename)
        image.save(image_filename)
        print(f"Image saved: {image_filename}")
    if voice and voice.filename:
        voice_filename = os.path.join('uploads/voices', voice.filename)
        voice.save(voice_filename)
        print(f"Voice saved: {voice_filename}")

    try:
        with open('submissions.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([name, phone, location, problem, help_type, image_filename, voice_filename])
        print("Write to CSV successful.")
    except Exception as e:
        print(f"Error writing to CSV: {e}")

    return 'Request Received! Thank you.'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


