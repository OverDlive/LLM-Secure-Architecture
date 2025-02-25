from flask import Flask, render_template
import os

# 'ubuntu' 폴더를 포함하도록 경로 수정
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Front', 'static')
template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Front', 'templates')

app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)