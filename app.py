# app.py

from flask import Flask, request, jsonify
from flask.views import View
from flask_restx import Api, Resource, Namespace

import models
from create_data import genre
from models import *
from config import *

api: Api = Api(app, description='Movies API')

# Создаю namespaces
movies_ns: Namespace = api.namespace('movies')
directors_ns: Namespace = api.namespace('directors')
genres_ns: Namespace = api.namespace('genres')


@movies_ns.route('/')
class MoviesView(Resource):

    def get(self):
        movies = db.session.query(models.Movie).all()
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        # представление возвращает только фильмы с определенным режиссером и жанром по запросу типа: /movies/?director_id=2&genre_id=4
        if director_id and genre_id:
            director_with_genre = movies_schema.dump(Movie.query.filter(Movie.director_id == director_id,
                                                          Movie.genre_id == genre_id).all())
            if director_with_genre == []:
                return f'Фильма с таким режиссёром №{director_id} и таким жанром №{genre_id} нет в базе', 404
            return director_with_genre, 200

        if director_id:
            director = movies_schema.dump(Movie.query.filter(Movie.director_id == director_id).all())
            if director == []:
                return f'Режиссёра с идентификатором №{director_id} нет в базе', 404
            return director, 200

        if genre_id:
            genre = movies_schema.dump(Movie.query.filter(Movie.genre_id == genre_id).all())
            if genre == []:
                return f'Жанра с идентификатором №{genre_id} нет в базе', 404
            return genre, 200

        else:
            return movies_schema.dump(movies), 200


@movies_ns.route('/<int:movie_id>')
class MovieView(Resource):
    def get(self, movie_id: int):
        movie = db.session.query(models.Movie).filter(models.Movie.id == movie_id).first()

        if movie is None:
            return f'Фильма с идентификатором №{movie_id} нет в базе', 404

        return movie_schema.dump(movie), 200

@directors_ns.route('/')
class DirectorsView(Resource):

    def get(self):
        directors = db.session.query(models.Director).all()
        return directors_schema.dump(directors), 200

@directors_ns.route('/<int:director_id>')
class DirectorView(Resource):

    def get(self, director_id):
        director = db.session.query(models.Director).filter(models.Director.id == director_id).first()
        if director is None:
            return f'Режиссёра с идентификатором №{director_id} нет в базе', 404

        return director_schema.dump(director), 200

@genres_ns.route('/')
class GenresView(Resource):

    def get(self):
        genres = db.session.query(models.Genre).all()
        return genres_schema.dump(genres), 200

@genres_ns.route('/<int:genre_id>')
class GenreView(Resource):

    def get(self, genre_id):
        genre = db.session.query(models.Genre).filter(models.Genre.id == genre_id).first()
        if genre is None:
            return f'Жанра с идентификатором №{genre_id} нет в базе', 404

        return genre_schema.dump(genre), 200


if __name__ == '__main__':
    app.run(debug=True)


