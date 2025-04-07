# 🎬 Movie Collection App 🍿

A Flask web application to manage your favorite movies, track ratings, and build your personal movie collection!

## ✨ Features

- 🔍 Search for movies using The Movie Database (TMDB) API
- 🌟 Rate movies on a scale of 1-10
- 📝 Write personal reviews for each movie
- 🏆 Automatically ranks movies based on your ratings
- 🖼️ Displays movie posters and details
- 🗑️ Delete movies from your collection
- ✏️ Edit ratings and reviews anytime

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- Flask
- SQLAlchemy
- Requests
- Flask-WTF
- Flask-Bootstrap5

### 🔧 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/movie-collection-app.git
   cd movie-collection-app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Get your API key from [The Movie Database](https://www.themoviedb.org/documentation/api):
   - Create an account
   - Request an API key
   - Replace `YOUR API KEY HERE` in the code with your actual API key

4. Set up your environment:
   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   ```

5. Run the application:
   ```bash
   flask run
   ```

6. 🌐 Open your browser and navigate to `http://localhost:5000`

## 💻 Usage

1. 🏠 **Home Page**: View your movie collection sorted by ranking
2. ➕ **Add Movie**: Search for movies by title
3. 🔍 **Select**: Choose the correct movie from search results
4. ⭐ **Rate**: Add your rating and review
5. 🗂️ **Manage**: Update ratings or delete movies from your collection

## 📁 File Structure

```
movie-collection-app/
├── app.py                  # Main Flask application
├── templates/              # HTML templates
│   ├── index.html          # Home page template
│   ├── add.html            # Add movie form
│   ├── select.html         # Movie selection page
│   └── edit.html           # Edit rating/review form
├── static/                 # Static files (CSS, JS)
└── top-movies-collection.db # SQLite database
```

## 🔐 Security Note

Remember to:
- Keep your API key private
- Use environment variables for sensitive information
- Change the Flask secret key in production

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [TMDB](https://www.themoviedb.org/) - For providing the movie API
- [Bootstrap](https://getbootstrap.com/) - For the frontend styling
- [SQLAlchemy](https://www.sqlalchemy.org/) - For database ORM

---

Happy movie collecting! 🎥 🍕 🎉
