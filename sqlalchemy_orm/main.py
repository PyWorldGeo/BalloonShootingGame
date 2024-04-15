#An ORM, or Object Relational Mapper, is a piece of software designed to translate between the data representations used by databases and those used in object-oriented programming.
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, joinedload, declarative_base, relationship
from sqlalchemy import Column, Integer, String, Boolean, CHAR, ForeignKey

Base = declarative_base()

class Person(Base):
    __tablename__ = "persons"

    ssn = Column("ssn", Integer, primary_key=True)
    firstname = Column("firstname", String)
    lastname = Column("lastname", String)
    gender = Column("gender", CHAR)
    age = Column("age", Integer)

    def __init__(self, ssn, firstname, lastname, gender, age):
        self.ssn = ssn
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.age = age

    def __repr__(self):
        return f"{self.ssn}, {self.firstname}, {self.lastname}, {self.gender}, {self.age}"

class Thing(Base):
    __tablename__ = "things"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    description = Column("description", String)
    owner = Column(Integer, ForeignKey("persons.ssn"), unique=True)


    def __init__(self, description, owner):
        self.description = description
        self.owner = owner


    def __repr__(self):
        return f"{self.id}, {self.description}, {self.owner}"

# engine = create_engine("sqlite:///mydb.db", echo=True)
#A SQLAlchemy engine is created by calling the create_engine function, passing it a Data Source Name (DSN). Note that echo=True is also passed here, this tells the engine object to log all the SQL it executed to sys.
engine = create_engine("sqlite:///")
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

person1 = Person(12342, "Nika", "Tsitskishvili", "M", 28)
person2 = Person(14523, "Elene", "Tskhadadze", "F", 22)
person3 = Person(22314, "Davit", "Mandjgaladze", "M", 26)
session.add(person1)
session.add(person2)
session.add(person3)
session.commit()

# session.add_all([person1, person2, person3])
# session.commit()

result = session.query(Person).all()
print(result)

result1 = session.query(Person).filter(Person.age == 28)
for r in result1:
    print(r)


result2 = session.query(Person).filter(Person.firstname.like("%e"))
for r in result2:
    print(r)

result3 = session.query(Person).filter(Person.firstname.in_(["Davit", "Lado"]))
for r in result3:
    print(r)


thing1 = Thing("Description 1", 12342)
thing2 = Thing("Description 2", 14523)
thing3 = Thing("Description 3", 22314)
session.add(thing1)
session.add(thing2)
session.add(thing3)
session.commit()

result = session.query(Thing).all()
print(result)

result10 = session.query(Thing, Person).filter(Thing.owner == Person.ssn).filter(Person.firstname == "Elene").all()
for r in result10:
    print(r)



session.query(Thing).filter(Thing.id==1).delete()
session.commit()
result = session.query(Thing).all()
print(result)


# connect to mysql
# pip install mysql-connector-python
from sqlalchemy import create_engine, text

# Connect to the database
engine = create_engine("mysql+mysqlconnector://root:DjagaDjango2024.@localhost/it_step")

# Test the connection
connection = engine.connect()

# result = connection.execute(text("SELECT * FROM customers"))
# for row in result:
#     print(row)

result = connection.execute(text("SELECT city FROM customers order by city limit 5"))
for row in result:
    print(row)

# session.delete(person1)
# session.commit()

# session.execute(text("DELETE from persons where id = 12376"))
# session.commit()













#https://medium.com/@shubhkarmanrathore/mastering-crud-operations-with-sqlalchemy-a-comprehensive-guide-a05cf70e5dea
#pip install sqlalchemy
# DATABASE_URL = "sqlite:///database.db"
# engine = create_engine(DATABASE_URL)
#
# Session = sessionmaker(bind=engine)
#
# session = Session()
#
# Base = declarative_base()
#
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     username = Column(String)
#     email = Column(String)
#
#
#
# # Create the table in the database
# Base.metadata.create_all(engine)
#
#
# # #Creating Data (C in CRUD)
# # new_user1 = User(username="john_doe", email="johndoe@example.com")
# # session.add(new_user1)
# # session.commit()
# # #
# # new_user2 = User(username="alice", email="alice@example.com")
# # session.add(new_user2)
# # session.commit()
#
# session.execute(text("SELECT * FROM users"))

# users = session.query(User).all()
#
# for user in users:
#     print(user)
#
#
# #Relationship
# from sqlalchemy import ForeignKey
# from sqlalchemy.orm import relationship
#
# class Task(Base):
#     __tablename__ = "tasks"
#
#     id = Column(Integer, primary_key=True)
#     title = Column(String)
#     user_id = Column(Integer, ForeignKey("users.id"))
#
#     # Establish the relationship to the User model
#     user = relationship("User", back_populates="tasks")
#
# class User(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True)
#     username = Column(String)
#     email = Column(String)
#
#     # Establish the reverse relationship to tasks
#     tasks = relationship("Task", back_populates="user")
#
#
# # inserting records with relationships
# user = User(username="jane", email="jane@example.com")
# task = Task(title="Complete project", user=user)
#
# session.add(user)
# session.add(task)
# session.commit()
#
#
#
# #Reading Data
# # Retrieve all users
# users = session.query(User).all()
#
# # Retrieve a single user by id
# user = session.query(User).get(1)
#
#
# # Retrieve users with a specific email
# users = session.query(User).filter_by(email="johndoe@example.com").all()
#
# # Retrieve users whose usernames start with 'j' and sort by username
# users = session.query(User).filter(User.username.startswith("j")).order_by(User.username).all()
#
#
#
# from sqlalchemy import func
#
# # Count the number of users
# user_count = session.query(func.count(User.id)).scalar()
#
# # Retrieve users and their associated tasks using a join
# users_with_tasks = session.query(User, Task).join(Task).all()
#
#
# #Updating Data (U in CRUD)
# # Query a user by id
# user = session.query(User).get(1)
#
# # Update the user's email
# user.email = "new_email@example.com"
#
# # Commit the changes
# session.commit()
#
#
# # Update all users with a certain username
# session.query(User).filter_by(username="old_username").update({"username": "new_username"})
# session.commit()
#
# try:
#     # Begin a transaction
#     session.begin()
#
#     # Update user data
#     user.email = "updated_email@example.com"
#     session.commit()  # Commit the transaction
# except:
#     session.rollback()  # Rollback if an error occurs
#
#
#
#
# #Deleting Data (D in CRUD)
# # Query a user by id
# user = session.query(User).get(1)
#
# # Delete the user
# session.delete(user)
# session.commit()
#
#
# class User(Base):
#     # ...
#
#     tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
#
# class User(Base):
#     # ...
#
#     is_deleted = Column(Boolean, default=False)
#
# #Error Handling and Data Validation
# from sqlalchemy.exc import SQLAlchemyError
#
# try:
#     # Database operation
#     session.commit()
# except SQLAlchemyError as e:
#     session.rollback()  # Rollback on error
#     print(f"An error occurred: {e}")
#
#
#
#
#
# from sqlalchemy import Column, String, Integer
# from sqlalchemy.orm import validates
#
# class User(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True)
#     username = Column(String)
#     email = Column(String)
#
#     @validates("email")
#     def validate_email(self, key, email):
#         if "@" not in email:
#             raise ValueError("Invalid email address")
#         return email
#
#
#
# #Optimizing CRUD Operations
# # Fetch users and their tasks in one query
# users_with_tasks = session.query(User).options(joinedload(User.tasks)).all()
#
# # Bulk insert users
# new_users = [User(username="user1"), User(username="user2")]
# session.bulk_save_objects(new_users)
# session.commit()
#


