from extensions import db

class Employee(db.Model):
    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String)
    lastName = db.Column(db.String)
    address = db.Column(db.String)
    phone = db.Column(db.String)
    age = db.Column(db.Integer)
    hireDate = db.Column(db.String)
    terminationDate = db.Column(db.String)

    def __init__(self, firstName, lastName, address, phone, age, hireDate, terminationDate):
        self.firstName = firstName
        self.lastName = lastName
        self.address = address
        self.phone = phone
        self.age = age
        self.hireDate = hireDate
        self.terminationDate = terminationDate

    def serialize(self):
        return {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "address": self.address,
            "phone": self.phone,
            "age": self.age,
            "hireDate": self.hireDate,
            "terminationDate": self.terminationDate
        }

