from pydantic import BaseModel


class RepositoryCreate(BaseModel):
    name: str
    github_url: str
    description: str

class RepositoryResponse(BaseModel):
    id: int
    name: str
    github_url: str
    description: str

    class Config:
        from_attributes = True