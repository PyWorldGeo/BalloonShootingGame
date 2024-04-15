from models import session, Address, User, FacebookUser
#one to many
#creating users
# user1 = User(name="Giorgi Lezava", age=23)
# user2 = User(name="Nino Khetaguri", age=25)
#
# #create addresses
# address1 = Address(city="Tbilisi", state="Saburtalo", zip_code="0261")
# address2 = Address(city="Tbilisi", state="Vake", zip_code="0261")
# address3 = Address(city="Batumi Boulevard", state="Saburtalo", zip_code="0261")
#
# #Associating addresses with users
# user1.addresses.extend([address1, address2])
# user2.addresses.append(address3)
#
# #add users and addresses to database
# session.add(user1)
# session.add(user2)
# session.commit()
#
# print(f"{user1.addresses}")
# print(f"{user2.addresses}")

#self relationship
#creating users
user1 = FacebookUser(username="Lado222")
user2 = FacebookUser(username="Nincho18")
user3 = FacebookUser(username="DonVito21")


#Associating addresses with users
user1.following.append(user2)
user2.following.append(user3)
# user3.following.append(user1)


#add users and addresses to database
session.add_all([user1, user2, user3])
session.commit()

print(f"{user1.following = }")
print(f"{user2.following = }")
print(f"{user3.following = }")


