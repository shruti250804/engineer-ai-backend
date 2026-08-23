from pydantic import BaseModel, Field, HttpUrl, EmailStr

class RepositoryCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    github_url: HttpUrl
    description: str = Field(min_length=5, max_length=500)


class RepositoryResponse(BaseModel):
    id: int
    name: str
    github_url: str
    description: str

    class Config:
        from_attributes = True
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

