
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import engine, SessionLocal, get_db
from . import models
from .schemas import RepositoryCreate
from .models import Repository

app=FastAPI()
models.Base.metadata.create_all(bind=engine)

@app.post("/repositories")
def create_repository(
    repository: RepositoryCreate,
    db: Session = Depends(get_db)
):
    db_repo = Repository(
        name=repository.name,
        github_url=repository.github_url,
        description=repository.description
    )

    db.add(db_repo)
    db.commit()
    db.refresh(db_repo)

    return db_repo

