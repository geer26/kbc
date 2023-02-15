from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    #return "Hello, World!"
    context = 'HELLO FROM FLASK!'
    return render_template('index.html', title='Home', m_from_flask=context)