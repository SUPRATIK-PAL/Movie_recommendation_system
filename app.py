from flask import Flask, request, redirect, url_for, render_template

import recommender as rec
from movie_detail_grabber import grab_movie_details


app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")

@app.route("/recommend", methods=['POST'])
def get_movie_name():
    global movie_name
    global recommended_movies
    movie_name = request.form.get('movie_name')
    recommended_movies = rec.get_movie_recommendation(movie_name)
    return redirect(url_for('show_recommended_movies'))

@app.route("/recommendations", methods=['GET'])
def show_recommended_movies():
    detailed_movies = []
    for movie in recommended_movies:
        detailed_movies.append(grab_movie_details(movie))

    print(detailed_movies)

    return render_template("recommendations.html", movie_name=movie_name, recommended_movies=detailed_movies)

if __name__ == '__main__':
   app.run(debug = True)