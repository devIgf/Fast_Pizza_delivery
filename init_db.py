from database import Base, engine
from models import User, Order


Base.metadata.create_all(bind=engine)
# This code creates all the tables in the database defined by the models in models.py.