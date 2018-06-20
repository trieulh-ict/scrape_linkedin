from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()



engine = create_engine('mysql+pymysql://root:123456@localhost')

Base.metadata.create_all(engine)
