from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, joinedload, declarative_base, relationship, Mapped, mapped_column
from sqlalchemy import Column, Integer, String, Boolean, CHAR, ForeignKey
# engine = create_engine("sqlite:///mydb.db")
engine = create_engine("sqlite:///")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    address = relationship("Address", back_populates="user", uselist=False) #class name with "" in case of imports


    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"
class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True)
    city = Column(String)
    user_id = Column(ForeignKey("users.id"))
    user = relationship("User", back_populates="address")

    def __repr__(self):
        return f"<Address(id={self.id}, city='{self.city}')>"




Base.metadata.create_all(bind=engine)

new_user = User(name="Nika", age=22)
new_address = Address(city="Tbilisi", user=new_user)
session.add(new_user)
session.add(new_address)
session.commit()