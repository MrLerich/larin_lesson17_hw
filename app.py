# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from models import *
from config import app

api = Api(app)

movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genre_ns = api.namespace('genre')

# Возвращает список всех фильмов наше БД
@movies_ns.route('/')
class MovieView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        # представление возвращает только фильмы с определенным режиссером и жанром по запросу типа: /movies/?director_id=2&genre_id=4
        if director_id and genre_id:
            query = movies_schema.dump(Movie.query.filter(Movie.director_id == director_id,
                                                           Movie.genre_id == genre_id).all())
            return query, 200

        if director_id:
            query = movies_schema.dump(Movie.query.filter(Movie.director_id == director_id).all())
            return query, 200

        if genre_id:
            query = movies_schema.dump(Movie.query.filter(Movie.genre_id == genre_id).all())
            return query, 200

@movies_ns.route('/<int:pk>')
class MovieView(Resource):
    def get(self, pk: int):
        return movies_schema.dump(Movie.query.get_or_404(pk)), 200






if __name__ == '__main__':
    app.run(debug=True)
