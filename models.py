from marshmallow import Schema, fields
from config import db


# Модель фильма
class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))

    genre = db.relationship("Genre")
    director = db.relationship("Director")


# Модель Жанра
class Director(db.Model):
    __tablename__ = 'director'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


# Модель Режисера
class Genre(db.Model):
    __tablename__ = 'genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


# Схема для получения полей сложной структуры
class DirectorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()

    genre = fields.Pluck('GenreSchema', 'name')
    director = fields.Pluck('DirectorSchema', 'name')


# Создам экземпляры схемы
movie_schema = MovieSchema()  # для одного поля
movies_schema = MovieSchema(many=True)  # для нескольких полей

director_schema = DirectorSchema()  # для одного поля
directors_schema = DirectorSchema(many=True)  # для нескольких полей

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)  # для нескольких полей
