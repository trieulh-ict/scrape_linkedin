import json

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    linkedin_id = Column(String(250), primary_key=True, nullable=False)
    name = Column(Text)
    school = Column(Text)
    headline = Column(Text)
    company = Column(Text)
    summary = Column(Text)
    location = Column(Text)
    skills = relationship('Skill', backref='user')
    accomplishments = relationship('Accomplishment', backref='user')
    educations = relationship('Education', backref='user')
    jobs = relationship('Job', backref='user')
    volunteerings = relationship('Volunteering', backref='user')


class Education(Base):
    __tablename__ = 'education'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    activities = Column(Text)
    name = Column(Text)
    degree = Column(Text)
    field_of_study = Column(Text)
    date_range = Column(Text)
    grades = Column(Text)


class Job(Base):
    __tablename__ = 'job'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    company = Column(Text)
    title = Column(Text)
    description = Column(Text)
    location = Column(Text)
    date_range = Column(Text)


class Volunteering(Base):
    __tablename__ = 'volunteering'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    company = Column(Text)
    title = Column(Text)
    description = Column(Text)
    location = Column(Text)
    date_range = Column(Text)
    cause = Column(Text)


class Skill(Base):
    __tablename__ = 'skill'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    name = Column(Text, nullable=False)


class Accomplishment(Base):
    __tablename__ = 'accomplishment'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    name = Column(Text, nullable=False)
    category = Column(Text, nullable=False)


engine = create_engine('mysql+pymysql://root:123456@localhost/linkedin?charset=utf8', encoding='utf-8')

Base.metadata.create_all(engine)
