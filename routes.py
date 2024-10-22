from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from extensions import db, bcrypt
from models import User, Message

def register_routes(app):
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Cadastro realizado com sucesso! Você pode fazer login agora.', 'success')
            return redirect(url_for('login'))

        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST': 
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('chat'))
            else:
                flash('Login falhou. Verifique o email e a senha.', 'danger')
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/chat')
    @login_required
    def chat():
        messages = Message.query.order_by(Message.date_posted.desc()).all()
        return render_template('chat.html', messages=messages)

    @app.route('/send_message', methods=['POST'])
    @login_required
    def send_message():
        content = request.form.get('message')
        message = Message(content=content, user_id=current_user.id)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('chat'))