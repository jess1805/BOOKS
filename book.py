from flask import Flask, flash, redirect, render_template, url_for 
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class fbook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), unique=True, nullable=False)
    author = db.Column(db.String(20), unique=True, nullable=False)
    genre = db.Column(db.String(50), unique=True, nullable=False)
    rating = db.Column(db.Float, default='0.0')

def __repr__(self):
        return f"Book('{self.title}', '{self.author}', '{self.genre}')"

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(60), nullable=False)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        title = form.title.data
        author = form.author.data
        genre = form.genre.data
        rating = form.rating.data
        hashed_password = Bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = fbook(title=title, author=author, genre=genre, rating=rating)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = fbook.query.filter_by(title=form.title.data).first()
        if user and Bcrypt.check_password_hash(user.password, form.password.data):
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check title and password', 'danger')
    return render_template('login.html', title = 'Login')


  
if __name__=='__main__': 
   app.run( debug = True) 


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField
from flask_wtf.file import DataRequired
from wtforms.validators import Email

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()]) 
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
