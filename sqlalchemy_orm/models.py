from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, joinedload, declarative_base, relationship, Mapped, mapped_column
from sqlalchemy import Column, Integer, String, Boolean, CHAR, ForeignKey
# engine = create_engine("sqlite:///mydb.db")
engine = create_engine("sqlite:///")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
#non mapped one-to-many (one user can have many addresses)
class BaseModel(Base):
    __abstract__ = True #allow other classes to inherit from this without creating table
    __allow_unmapped__ = True
    id = Column(Integer, primary_key=True)


class Address(BaseModel):
    __tablename__ = "addresses"

    city = Column(String)
    state = Column(String)
    zip_code = Column(Integer)

    user_id = Column(ForeignKey("users.id"))

    def __repr__(self):
        return f"<Address(id={self.id}, city='{self.city}')>"

class User(BaseModel):
    __tablename__ = "users"

    name = Column(String)
    age = Column(Integer)
    addresses = relationship(Address) #class name with "" in case of imports

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"

Base.metadata.create_all(bind=engine)

#non mapped one-to-many (backward relationship)
class BaseModel(Base):
    __abstract__ = True #allow other classes to inherit from this without creating table
    __allow_unmapped__ = True
    id = Column(Integer, primary_key=True)


class Address(BaseModel):
    __tablename__ = "addresses"

    city = Column(String)
    state = Column(String)
    zip_code = Column(Integer)

    user_id = Column(ForeignKey("users.id"))

    #adding
    #user = relationship("User") SAWarning: relationship 'User.addresses' will copy column users.id to column addresses.user_id
    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"<Address(id={self.id}, city='{self.city}')>"

class User(BaseModel):
    __tablename__ = "users"

    name = Column(String)
    age = Column(Integer)
    addresses = relationship("Address") #class name with "" in case of imports

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"

Base.metadata.create_all(bind=engine)

#mapped
class BaseModel(Base):
    __abstract__ = True #allow other classes to inherit from this without creating table
    __allow_unmapped__ = True
    id = Column(Integer, primary_key=True)


class Address(BaseModel):
    __tablename__ = "addresses"

    city = Column(String)
    state = Column(String)
    zip_code = Column(Integer)
    #Change
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="addresses")

    def __repr__(self):
        return f"<Address(id={self.id}, city='{self.city}')>"

class User(BaseModel):
    __tablename__ = "users"

    name = Column(String)
    age = Column(Integer)
    #Change
    addresses: Mapped[list["Address"]] = relationship()

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"

Base.metadata.create_all(bind=engine)


# self relationship
class FacebookUser(Base):
    __tablename__ = "facebook_users"
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True)
    username = Column(String)
    following_id = Column(Integer, ForeignKey("facebook_users.id"))
    following = relationship('FacebookUser', remote_side=[id], uselist=True) #if we dont want one-to-one relationship, we must pass uselist

    def __repr__(self):
        return f"<FacebookUser(id={self.id}, username='{self.username}, following={self.following}')>"

Base.metadata.create_all(bind=engine)

#this code has circular dependency issue

#solve problem
class FollowingAssociation(BaseModel):
    __tablename__ = "following_association"

    user_id = Column(Integer, ForeignKey('facebook_users.id'))
    following_id = Column(Integer, ForeignKey('facebook_users.id'))

class FacebookUser(Base):
    __tablename__ = "facebook_users"
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True)
    username = Column(String)
    following_id = Column(Integer, ForeignKey("facebook_users.id"))
    following = relationship('FacebookUser', secondary="following_association", primaryjoin=("FollowingAssociation.user_id==FacebookUser.id"), secondaryjoin=("FollowingAssociation.following_id==FacebookUser.id"))

    def __repr__(self):
        return f"<FacebookUser(id={self.id}, username='{self.username}, following={self.following}')>"

Base.metadata.create_all(bind=engine)