from pydantic import BaseModel


class RepositoryCreate(BaseModel):
    name: str
    github_url: str
    description: str