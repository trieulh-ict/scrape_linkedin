import json
from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker
from setup import Base, Skill, User, UserSkill

engine = create_engine('mysql+pymysql://root:123456@localhost/linkedin')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

with open('profiles.json') as file:
    data = json.load(file)

    for user_id in data:
        user = data[user_id]
        user_profile = user['personal_info']

        # Insert to db
        new_user = session.query(User).filter(User.linkedin_id == user_id).first()
        if not new_user:
            new_user = User(linkedin_id=user_id)

        #Add Skill
        user_skills = user['skills']
        for item in user_skills:
            skill = session.query(Skill).filter(Skill.name == item['name']).first()
            if not skill:
                skill = Skill(name=item['name'])

            if not session.query(UserSkill).filter(
                    UserSkill.user_id == new_user.id and UserSkill.skill_id == skill.id).first():
                user_skill = UserSkill(user=new_user, skill=skill, endorsement=int(item['endorsements']))
                session.add(user_skill)

        session.commit()

        # session.commit()
