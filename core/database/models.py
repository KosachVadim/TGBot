from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Country(Base):
    __tablename__ = 'core_country'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    tag = Column(String(10), unique=True, nullable=False)

    def __str__(self):
        return self.name

class Manager(Base):
    __tablename__ = 'core_manager'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    tg = Column(String(255), nullable=False)

    def __str__(self):
        return self.tg
class Vacancy(Base):
    __tablename__ = 'core_vacancy'

    id = Column(Integer, primary_key=True, autoincrement=True)
    country_id = Column(Integer, ForeignKey('core_country.id'))
    city = Column(String(255), nullable=False)
    specialization = Column(String(255), nullable=False)
    salary = Column(String(255), nullable=False)
    language = Column(String(255), nullable=False)
    manager_account_id = Column(Integer, ForeignKey('core_manager.id'))
    for_whom = Column(String(255), nullable=True)
    chart = Column(Text, nullable=True)
    housing = Column(String(255), nullable=True)
    work_clothes = Column(String(255), nullable=True)
    getting_to_work = Column(String(255), nullable=True)
    responsibilities = Column(Text, nullable=True)
    requirements = Column(Text, nullable=True)
    unique_id = Column(String(10), unique=True, default='', nullable=False)

    country = relationship('Country', backref='vacancies')
    manager_account = relationship('Manager', backref='vacancies')


class User(Base):
    __tablename__ = 'core_user'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    def __str__(self):
        return self.name

class Resume(Base):
    __tablename__ = 'core_resume'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('core_user.id'))
    nationality = Column(String(50), nullable=True)
    experience_job_title = Column(String(100), nullable=True)
    experience_duration_years = Column(String(100), nullable=True)
    experience_description = Column(Text, nullable=True)
    user = relationship('User', backref='users')

    def __str__(self):
        return f"Resume for {self.user.name}"

