from flask import Flask, request, render_template, redirect, url_for, send_file
import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set the maximum age of uploaded files in seconds (2 weeks)
MAX_FILE_AGE = 14 * 24 * 60 * 60

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'brandonwandrie@gmail.com'
SMTP_PASSWORD = 'jaluqmpmxfduuwnb'
EMAIL_FROM = 'brandonwandrie@gmail.com'
EMAIL_TO = 'brandonwandrie@gmail.com'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file:
        return 'No file uploaded! <a href="/">Return to homepage</a>'
    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    # Email details of the uploaded file
    email_subject = f'New file uploaded: {filename}'
    email_body = f'Filename: {filename}\nSize: {os.path.getsize(file_path)} bytes\nLink: {url_for("download", filename=filename, _external=True)}'
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = email_subject
    msg.attach(MIMEText(email_body))
    
    with open(file_path, 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype=os.path.splitext(filename)[1][1:])
        attachment.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(attachment)
    
    smtp_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp_server.starttls()
    smtp_server.login(SMTP_USERNAME, SMTP_PASSWORD)
    smtp_server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    smtp_server.quit()
    
    return 'File uploaded successfully! <a href="/">Return to homepage</a>'

@app.route('/download/<filename>')
def download(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.isfile(file_path):
        return 'File not found! <a href="/">Return to homepage</a>'
    return send_file(file_path, as_attachment=True)

@app.route('/cleanup')
def cleanup():
    now = time.time()
    for file_name in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        if os.path.isfile(file_path) and now - os.path.getmtime(file_path) > MAX_FILE_AGE:
            os.remove(file_path)
    return f'Deleted old files. <a href="/">Return to homepage</a>'

if __name__ == '__main__':
    app.run()
