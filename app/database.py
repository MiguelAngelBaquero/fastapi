from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# If you have both your app and dabase inside docker containers
# you need to know the real ip address of the database container 
# This is due to the default network mode on docker, bridge.
# If you are running tests on your local machine switch the ip
# address back to 'localhost'.
URL_DATABASE = 'postgresql://postgres:root@172.17.0.2:5432/my_collections'
# URL_DATABASE = 'postgresql://postgres:root@localhost:5432/my_collections'

# Sync
engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()