from pydantic import BaseModel, StrictStr, PositiveInt, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import Optional
from datetime import date, datetime
from pydantic.functional_validators import BeforeValidator
from typing import Annotated

def parse_custom_date(value):
    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%d/%m/%Y").date()
        except ValueError:
            raise ValueError("Date must be in DD/MM/YYYY format")
    return value

CustomDate = Annotated[date, BeforeValidator(parse_custom_date)]

class EmployeeCreate(BaseModel):
    firstName: StrictStr
    lastName: StrictStr
    address: StrictStr
    phone: PhoneNumber
    age: PositiveInt
    hireDate: CustomDate
    terminationDate: Optional[CustomDate] = None

    def serialize(self):
        return {
            'firstName': self.firstName,
            'lastName': self.lastName,
            'address': self.address,
            'phone': self.phone,
            'age': self.age,
            'hireDate': self.hireDate.strftime("%d/%m/%Y"),
            'terminationDate': self.terminationDate.strftime("%d/%m/%Y") if self.terminationDate is not None else None
        }
    
class EmployeeSearch(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    minAge: Optional[int] = None
    maxAge: Optional[int] = None
    
class EmployeeUpdate(BaseModel):
    firstName: StrictStr
    lastName: StrictStr
    address: StrictStr
    phone: PhoneNumber
    age: PositiveInt
    hireDate: CustomDate
    terminationDate: Optional[CustomDate] = None

    def serialize(self):
        return {
            'firstName': self.firstName,
            'lastName': self.lastName,
            'address': self.address,
            'phone': self.phone,
            'age': self.age,
            'hireDate': self.hireDate.strftime("%d/%m/%Y"),
            'terminationDate': self.terminationDate.strftime("%d/%m/%Y") if self.terminationDate is not None else None
        }