from flask import Flask, render_template
import os

# 'ubuntu' 폴더를 포함하도록 경로 수정
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ubuntu', 'static')
template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ubuntu', 'templates')

snort = Flask(__name__, static_folder=static_folder, template_folder=template_folder)

snort.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
snort.config['TEMPLATES_AUTO_RELOAD'] = True

@snort.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    snort.run(debug=True)