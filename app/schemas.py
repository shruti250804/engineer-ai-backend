from pydantic import BaseModel, Field, HttpUrl

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