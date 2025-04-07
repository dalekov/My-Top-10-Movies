from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
import requests

# API constants for The Movie Database (TMDB)
MOVIE_DB_API_KEY = "YOUR API KEY HERE"
MOVIE_DB_AUTH_TOKEN = "YOUR AUTH TOKEN HERE"
MOVIE_DB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
MOVIE_DB_MOVIE_DETAILS_URL = "https://api.themoviedb.org/3/movie/{movie_id}"

# Initialize Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR SECRET KEY HERE'  # Secret key for session security
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///top-movies-collection.db'  # SQLite database location
Bootstrap5(app)  # Initialize Bootstrap for styling


# Create database base class
class Base(DeclarativeBase):
    pass


# Initialize SQLAlchemy with the base class
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Define Movie database model
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # Primary key for the movie
    title: Mapped[str] = mapped_column(String(250), unique=True)  # Movie title (unique)
    year: Mapped[int] = mapped_column(Integer, nullable=False)  # Release year
    description: Mapped[str] = mapped_column(String(500), nullable=False)  # Movie description/overview
    rating: Mapped[float] = mapped_column(Float, nullable=False)  # User rating (out of 10)
    ranking: Mapped[int] = mapped_column(Integer, nullable=False)  # Ranking position in the collection
    review: Mapped[str] = mapped_column(String(250), nullable=False)  # User review text
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)  # Movie poster image URL


# Create database tables within the application context
with app.app_context():
    db.create_all()


# Form for editing movie ratings and reviews
class EditForm(FlaskForm):
    new_rating = FloatField(label='Your Rating Out of 10, e.g. 7.5', validators=[DataRequired()])  # Rating input field
    new_review = StringField(label='Your Review', validators=[DataRequired()])  # Review input field
    submit = SubmitField(label='Done')  # Submit button


# Form for adding a new movie by title
class AddMovieForm(FlaskForm):
    title = StringField(label='Movie Title', validators=[DataRequired()])  # Movie title input field
    submit = SubmitField(label='Add Movie')  # Submit button


# Home route - displays all movies sorted by rating
@app.route("/")
def home():
    # Query the database for all movies ordered by rating (lowest to highest)
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    all_movies = result.scalars().all()

    # Update rankings based on rating (highest rating gets lowest ranking number)
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i  # Reverse order: highest rating = ranking 1
    db.session.commit()  # Save ranking changes to database

    # Render the home page with the list of movies
    return render_template("index.html", movies=all_movies)


# Route for updating a movie's rating and review
@app.route("/update/<int:index>", methods=['GET', 'POST'])
def update(index):
    # Find the movie by ID or return 404 if not found
    selected_movie = Movie.query.get_or_404(index)
    edit_form = EditForm()  # Create the edit form

    # If form is submitted and validated
    if edit_form.validate_on_submit():
        # Update the movie with new rating and review
        selected_movie.rating = float(edit_form.new_rating.data)
        selected_movie.review = edit_form.new_review.data
        db.session.commit()  # Save changes to database
        return redirect(url_for('home'))  # Redirect back to home page

    # Display the edit form
    return render_template('edit.html', form=edit_form)


# Route for deleting a movie
@app.route('/delete/<int:index>', methods=["GET", "POST"])
def delete(index):
    # Find the movie by ID or return 404 if not found
    selected_movie = Movie.query.get_or_404(index)
    db.session.delete(selected_movie)  # Delete the movie
    db.session.commit()  # Save changes to database

    # Redirect back to home page
    return redirect(url_for('home'))


# Route for adding a new movie (search by title)
@app.route("/add", methods=["GET", "POST"])
def add_movie():
    form = AddMovieForm()  # Create the add movie form

    # If form is submitted and validated
    if form.validate_on_submit():
        movie_title = form.title.data  # Get the movie title from the form

        # Search TMDB API for movies matching the title
        response = requests.get(MOVIE_DB_SEARCH_URL, params={"api_key": MOVIE_DB_API_KEY, "query": movie_title})
        data = response.json()["results"]  # Get search results

        # Display search results for user selection
        return render_template("select.html", options=data)

    # Display the add movie form
    return render_template("add.html", form=form)


# Route for selecting a specific movie from search results
@app.route("/select/<int:index>", methods=["GET", "POST"])
def select_movie(index):
    # Get detailed information about the selected movie from TMDB API
    response = requests.get(
        MOVIE_DB_MOVIE_DETAILS_URL.format(movie_id=index),
        params={"api_key": MOVIE_DB_API_KEY}
    )
    data = response.json()  # Get movie details

    print(data)  # Debug: print movie data to console

    # Create a new Movie object with data from the API
    new_movie = Movie(
        title=data["title"],
        year=int(data["release_date"].split('-')[0]),  # Extract year from release date
        description=data["overview"],
        rating=0,  # Default rating until user reviews
        ranking=0.0,  # Default ranking until home page updates it
        review="Not reviewed yet.",  # Default review until user updates
        img_url=f"https://image.tmdb.org/t/p/w500{data['poster_path']}"  # Construct poster image URL
    )

    # Add the new movie to the database
    db.session.add(new_movie)
    db.session.commit()

    # Redirect back to home page
    return redirect(url_for('home'))


# Run the application in debug mode if executed directly
if __name__ == '__main__':
    app.run(debug=True)