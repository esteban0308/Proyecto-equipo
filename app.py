from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email')
        password = request.form.get('password')

        return redirect('http://127.0.0.1:5000S')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre   = request.form.get('nombre')
        email    = request.form.get('email')
        negocio  = request.form.get('negocio')
        password = request.form.get('password')

        return redirect(url_for('login'))

    return render_template('register.html')