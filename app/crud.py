from sqlalchemy.orm import Session

import models, schemas

def create_movie(db: Session, movie: schemas.MovieCreate):
  _movie = models.Movie(author = movie.author, description = movie.description, release_date = movie.release_date)
  db.add(_movie)
  db.commit()
  db.refresh(_movie)
  return 'Id: ' + str(_movie.id)

def get_movie_by_description(db: Session, description: str):
  return db.query(models.Movie).filter(models.Movie.description == description).first()

def get_movie(db: Session, movie_id: int):
  return db.query(models.Movie).filter(models.Movie.id == movie_id).first()

def delete_movie(db: Session, movie_id: int):
  _movie = get_movie(db, movie_id = movie_id)
  db.delete(_movie)
  db.commit()
  return 'Id: ' + str(_movie.id)

def get_movies(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.Movie).offset(skip).limit(limit).all()