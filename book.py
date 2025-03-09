from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float, nullable=True)

    def __init__(self, title, author, genre, rating):
        if not title or not author or not genre:
            raise ValueError("Title, author, and genre are required.")
        if rating is not None and (rating < 1 or rating > 5):
            raise ValueError("Rating must be between 1 and 5.")
        
        self.title = title
        self.author = author
        self.genre = genre
        self.rating = rating

with app.app_context():
    db.create_all()

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Book not found'}), 404

@app.errorhandler(ValueError)
def validation_error(error):
    return jsonify({'error': str(error)}), 400

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    try:
        book = Book(**data)
        db.session.add(book)
        db.session.commit()
        return jsonify({'message': 'Book added successfully!', 'id': book.id}), 201
    except ValueError as e:
        return validation_error(e)

@app.route('/books', methods=['GET'])
def get_books():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    genre = request.args.get('genre')
    rating = request.args.get('rating', type=float)
    
    query = Book.query
    if genre:
        query = query.filter(Book.genre.ilike(f'%{genre}%'))
    if rating is not None:
        query = query.filter(Book.rating >= rating)
    
    books_paginated = query.paginate(page=page, per_page=limit, error_out=False)
    books_list = [{'id': book.id, 'title': book.title, 'author': book.author, 'genre': book.genre, 'rating': book.rating} for book in books_paginated.items]
    return jsonify(books_list)

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author, 'genre': book.genre, 'rating': book.rating})

if __name__ == '__main__':
    app.run(debug=True)



#from flask_wtf import FlaskForm
#from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField
#from flask_wtf.file import DataRequired
#from wtforms.validators import Email

#class RegistrationForm(FlaskForm):
 #   username = StringField('Username', validators=[DataRequired()])
 #   email = StringField('Email', validators=[DataRequired(), Email()])
#  password = PasswordField('Password', validators=[DataRequired()])
  #  submit = SubmitField('Sign Up')

#class LoginForm(FlaskForm):
 #   username = StringField('Username', validators=[DataRequired()]) 
  #  password = PasswordField('Password', validators=[DataRequired()])
   # submit = SubmitField('Login')
