import json

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class UserSkill(Base):
    __tablename__ = 'user_skill'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    skill_id = Column(Integer, ForeignKey('skill.id'), primary_key=True)
    endorsement = Column(Integer, default=0)
    user = relationship("User", backref="user")
    skill = relationship("Skill")


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    linkedin_id = Column(String(250), nullable=False)
    name = Column(String(250))
    school = Column(String(250))
    headline = Column(String(250))
    company = Column(String(250))
    summary = Column(String(250))
    location = Column(String(250))
    skills = relationship("UserSkill")

class Skill(Base):
    __tablename__ = 'skill'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


engine = create_engine('mysql+pymysql://root:123456@localhost/linkedin')

Base.metadata.create_all(engine)
