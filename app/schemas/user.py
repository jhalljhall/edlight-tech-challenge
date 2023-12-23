from typing import List, Optional
from pydantic import BaseModel, EmailStr

from app.schemas.review import Review
# from app.schemas.tag import Tag

#* schema notes
# using pydantic models - help define structure of user data
    #! specifying which fields are required/optional + how to be validated

    #! "user" as in the perspective of the data that the API recieves from the client (user input during creation or update)
    #! - and the data that the API returns to the client - user data in API response

# Shared properties
    # represents the shared properties of a user
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    username: Optional[str] = None

# Properties to receive via API on creation
    #extend userbase - defines properties to recieve via API during user creation
    #data that the user provides! - structure + validation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
    #extend userbase - defines properties to recieve via API during user creation
    #data that the user provides! - structure + validation
class UserUpdate(UserBase):
    password: Optional[str] = None

    # used for additional prroperties stored in the database
class UserInDBBase(UserBase):
    id: Optional[int] = None

    # purpose of Config class in pydantic is to customize behavior of the model
    # from_attributes - contols how pydantic initializes model instances
        # when set to true - pydantic considerrs the fields (class attributes) declared in the class as valid attributes for the model...?
        #? confused why this is only needed here? - when do i need this?
    class Config:
        from_attributes = True


# Additional properties to return via API
    #is used for additional properties to return via the API - doesn't add any new fields but can be extended
    #* pass - is a placeholder that does nothing
    # User class is inheriting from UserInDBBase but not adding any additional properties
class User(UserInDBBase):

    # tags: List["Tag"]
    #badges: List["B"]
    reviews: List["Review"]
    #collection: List["C"]
    #! check this later


# Additional properties stored in DB
    #represents structure of user data as it is stored in the database
    #includes additional details that might not be exposed to user but crucial for app's internal functionality
class UserInDB(UserInDBBase):
    hashed_password: str
