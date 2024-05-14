# import libraries
from fastapi import FastAPI, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from typing import List, Annotated
from sqlalchemy.orm import Session

# import modules from current project
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# create movies
@app.post('/movies', response_model=schemas.Response)
async def create_movie(db: db_dependency, movie: schemas.MovieCreate):
  _movie = crud.get_movie_by_description(db, description = movie.description)
  if _movie:
    raise HTTPException(status_code=400, detail='Movie already registered')
  response = crud.create_movie(db = db, movie = movie)
  return schemas.Response(code=200, status="OK", message="Movie created", result= response).dict(exclude_none=True)

# read movie
@app.get('/movies/{movie_id}', response_model=schemas.Movie)
async def read_movie(movie_id: int, db: db_dependency):
  _movie = crud.get_movie(db, movie_id=movie_id)
  if not _movie:
    raise HTTPException(status_code=404, detail='Movie not found')
  return _movie

# delete movie
@app.delete('/movies/{movie_id}', response_model=schemas.Response)
async def delete_movie(movie_id: int, db: db_dependency):
  _movie = crud.get_movie(db, movie_id)
  if not _movie:
    raise HTTPException(status_code=404, detail='Movie not found')
  response = crud.delete_movie(db, movie_id)
  return schemas.Response(code=202, status="Deleted", message="Movie deleted", result= response).dict(exclude_none=True)

# update movie
@app.patch('/movies/{movie_id}', response_model=schemas.Movie)
async def patch_movie(movie_id: int, movie: schemas.MovieCreate, db: db_dependency):
  _movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
  if not _movie:
    raise HTTPException(status_code=404, detail='Movie not found')
  for key, value in movie.model_dump(exclude_unset=True).items():
    setattr(_movie, key, value)
  db.commit()
  return _movie

# read all movies
@app.get('/movies', response_model=list[schemas.Movie])
async def read_movies(db: db_dependency, skip: int = 0, limit : int = 100):
  _movies = crud.get_movies(db, skip=skip, limit=limit)
  if not _movies:
    raise HTTPException(status_code=404, detail='Movies not found')
  return _movies