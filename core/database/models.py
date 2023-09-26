from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Country(Base):
    __tablename__ = 'core_country'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    tag = Column(String(10), unique=True)

    def __str__(self):
        return self.name

class Person(Base):
    __tablename__ = 'core_person'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String)

    def __str__(self):
        return self.name

class Vacancy(Base):
    __tablename__ = 'core_vacancy'

    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey('core_country.id'))
    city = Column(String(255))
    specialization = Column(String(255))
    description = Column(Text)
    salary_range = Column(String(255))
    manager_account = Column(String(255))
    profit_type = Column(String(255))
    profit_amount = Column(Float)
    working_conditions = Column(Text)
    contact_person_id = Column(Integer, ForeignKey('core_person.id'))
    unique_id = Column(Integer, unique=True)

    country = relationship('Country', backref='vacancies')
    contact_person = relationship('Person', backref='contact_vacancies')
