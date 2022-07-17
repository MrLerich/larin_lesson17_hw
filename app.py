# app.py

from flask import Flask, request, jsonify
from flask_restx import Api, Resource, Namespace

import models
from models import *
from config import *

api: Api = Api(app, description='Movies API')

# Создаю namespaces
movies_ns: Namespace = api.namespace('movies')
directors_ns: Namespace = api.namespace('directors')
genre_ns: Namespace = api.namespace('genre')


@movies_ns.route('/')
class MoviesView(Resource):

    def get(self):
        movies = db.session.query(models.Movie).all()
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        # представление возвращает только фильмы с определенным режиссером и жанром по запросу типа: /movies/?director_id=2&genre_id=4
        if director_id and genre_id:
            query = movies_schema.dump(Movie.query.filter(Movie.director_id == director_id,
                                                          Movie.genre_id == genre_id).all())
            return query, 200

        if director_id:
            director = movies_schema.dump(Movie.query.filter(Movie.director_id == director_id).all())
            return director, 200

        if genre_id:
            genre = movies_schema.dump(Movie.query.filter(Movie.genre_id == genre_id).all())
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


if __name__ == '__main__':
    app.run(debug=True)
