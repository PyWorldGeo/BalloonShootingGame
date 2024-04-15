from sqlalchemy import create_engine, not_, or_, and_, func
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from random import choice

Base = declarative_base()

class Person(Base):
    __tablename__ = "persons"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    age = Column("age", Integer)

    def __init__(self, name, age):
        self.name = name
        self.age = age


    def __repr__(self):
        return f"Person(name={self.name}, age={self.age})"


engine = create_engine("sqlite:///:memory:")

Base.metadata.create_all(bind=engine)


names = ["Giorgi", "Mariami", "Elene", "Nika", "Daviti"]
ages = [22, 23, 18, 31, 40]

Session = sessionmaker(bind=engine)
session = Session()

for i in range(10):
    person = Person(choice(names), choice(ages))
    session.add(person)
    session.commit()

people = []
for i in range(15):
    person = Person(choice(names), choice(ages))
    people.append(person)

session.add_all(people)
session.commit()


all_persons = session.query(Person).all()
print(all_persons)

all_persons = session.query(Person).all()[0]
print(all_persons)


all_persons = session.query(Person).filter_by(name="Elene").all()

all_persons = session.query(Person).filter(Person.age > 22, Person.age < 30).all()

all_persons = session.query(Person).filter_by(name="Elene").one_or_none()

ele = session.query(Person).filter_by(name="Elene").first()

session.delete(all_persons)
ele.age = 55
session.commit()

print(session.query(Person).filter_by(name="Elene").all())

all_persons = session.query(Person).where(not_(Person.age >= 28) | (Person.name == "Nika")).all()
print(all_persons)

all_persons = session.query(Person).where((Person.age >= 28) & (Person.name == "Nika")).all()
print(all_persons)


all_persons = session.query(Person).filter(Person.name.in_(["Daviti", "Nika"])).all()
print(all_persons)

all_persons = session.query(Person).order_by(Person.age).all()
all_persons = session.query(Person).order_by(Person.age.desc()).all()
print(all_persons)

people = session.query(Person).all()
print(people)

people = session.query(Person.age).group_by(Person.age).all()
print(len(people))


people = session.query(Person.age, func.count(Person.id)).group_by(Person.age).all()
print(people)
