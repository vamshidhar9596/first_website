from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from datetime import datetime
import os

# Create Flask application
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.name}>'

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Message from {self.name}>'

# Forms
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=5, max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Send Message')

class SubscribeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Subscribe')

# Routes
@app.route('/')
def home():
    # Get recent messages for display
    recent_messages = Message.query.order_by(Message.created_at.desc()).limit(3).all()
    user_count = User.query.count()
    message_count = Message.query.count()
    
    return render_template('index.html', 
                         recent_messages=recent_messages,
                         user_count=user_count,
                         message_count=message_count)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    
    if form.validate_on_submit():
        # Save message to database
        message = Message(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(message)
        db.session.commit()
        
        flash('Thank you! Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html', form=form)

@app.route('/subscribe', methods=['POST'])
def subscribe():
    name = request.form.get('name')
    email = request.form.get('email')
    
    if name and email:
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        
        if existing_user:
            flash('You are already subscribed!', 'info')
        else:
            # Add new subscriber
            user = User(name=name, email=email)
            db.session.add(user)
            db.session.commit()
            flash('Successfully subscribed to our newsletter!', 'success')
    else:
        flash('Please fill in all fields!', 'error')
    
    return redirect(url_for('home'))

@app.route('/messages')
def messages():
    # Display all messages (admin view)
    all_messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template('messages.html', messages=all_messages)

@app.route('/subscribers')
def subscribers():
    # Display all subscribers (admin view)
    all_subscribers = User.query.order_by(User.created_at.desc()).all()
    return render_template('subscribers.html', subscribers=all_subscribers)

@app.route('/user/<name>')
def user(name):
    return f'<h1>Hello, {name}!</h1><p>Welcome to my website!</p><a href="/">Home</a>'

# Create database tables
if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
    
    app.run(debug=True, host='127.0.0.1', port=5000)