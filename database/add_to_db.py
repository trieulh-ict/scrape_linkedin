import json
from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker
from setup import Base, Skill, User, Accomplishment, Education, Job, Volunteering

engine = create_engine('mysql+pymysql://root:123456@localhost/linkedin?charset=utf8', encoding='utf-8')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine, autoflush=False)
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
        else:
            # Drop related skills
            skills = session.query(Skill).filter(Skill.user_id == new_user.id).all()
            for skill in skills:
                session.delete(skill)
            # Drop related accomplishments
            accomps = session.query(Accomplishment).filter(Accomplishment.user_id == new_user.id).all()
            for accomp in accomps:
                session.delete(accomp)
            # Drop related educations
            edus = session.query(Education).filter(Education.user_id == new_user.id).all()
            for edu in edus:
                session.delete(edu)
            # Drop related jobs
            jobs = session.query(Job).filter(Job.user_id == new_user.id).all()
            for job in jobs:
                session.delete(job)
            # Drop related volunteerings
            volunteerings = session.query(Volunteering).filter(Volunteering.user_id == new_user.id).all()
            for volunteering in volunteerings:
                session.delete(volunteering)

            session.commit()

        # Add Skills
        user_skills = user['skills']
        for item in user_skills:
            new_skill = Skill(name=item['name'])
            new_user.skills.append(new_skill)

        # Add Accomplishments
        user_accomps = user['accomplishments']
        for category in user_accomps:
            accomp_list = user_accomps[category]
            for accomp in accomp_list:
                new_accomp = Accomplishment(name=accomp, category=category)
                new_user.accomplishments.append(new_accomp)

        # Add Educations
        user_educations = user['experiences']['education']
        for edu in user_educations:
            new_edu = Education(activities=edu['activities'],
                                name=edu['name'],
                                degree=edu['degree'],
                                field_of_study=edu['field_of_study'],
                                date_range=edu['date_range'],
                                grades=edu['grades'])
            new_user.educations.append(new_edu)

        # Add Jobs
        user_jobs = user['experiences']['jobs']
        for job in user_jobs:
            new_job = Job(company=job['company'],
                          date_range=job['date_range'],
                          title=job['title'],
                          description=job['description'],
                          location=job['location'])
            new_user.jobs.append(new_job)

        # Add Volunteerings
        user_volunteerings = user['experiences']['volunteering']
        for volunteering in user_volunteerings:
            new_volunteering = Volunteering(company=volunteering['company'],
                                            date_range=volunteering['date_range'],
                                            title=volunteering['title'],
                                            description=volunteering['description'],
                                            location=volunteering['location'],
                                            cause=volunteering['cause'])
            new_user.volunteerings.append(new_volunteering)

        session.merge(new_user)
        session.commit()
