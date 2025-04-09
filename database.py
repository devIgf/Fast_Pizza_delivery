from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine("mysql+pymysql://root:@localhost:3306/pizza_delivery", echo=True)


Base = declarative_base()

SessionLocal = sessionmaker()