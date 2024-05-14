from pydantic import BaseModel
from typing import Optional, TypeVar, Generic
from pydantic.generics import GenericModel
from datetime import date

class MovieBase(BaseModel):
  author: Optional[str] = None
  description: Optional[str] = None
  release_date: Optional[date] = None

class MovieCreate(MovieBase):
  pass

class Movie(MovieBase):
  id: Optional[int] = None

  class Config:
    orm_mode = True

T = TypeVar('T')

class Response(GenericModel,Generic[T]):
    code: int
    status: str
    message: str
    result: Optional[T]=None