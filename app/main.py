from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import engine, SessionLocal, get_db
from . import models
from .schemas import RepositoryCreate, RepositoryResponse
from .models import Repository

app=FastAPI()
models.Base.metadata.create_all(bind=engine)

@app.post("/repositories",response_model=RepositoryResponse)
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

@app.get("/repositories", response_model=list[RepositoryResponse])
def get_repositories(
    db: Session = Depends(get_db)
):
    repositories = db.query(Repository).all()
    return repositories


# GET BY ID
@app.get("/repositories/{repo_id}",response_model=RepositoryResponse)
def get_repository(
    repo_id: int,
    db: Session = Depends(get_db)
):
    repo = db.query(Repository).filter(
        Repository.id == repo_id
    ).first()

    if repo is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found"
        )

    return repo

@app.put("/repositories/{repo_id}",response_model=RepositoryResponse)
def update_repository(
    repo_id: int,
    repository: RepositoryCreate,
    db: Session = Depends(get_db)
):
    repo = db.query(Repository).filter(
        Repository.id == repo_id
    ).first()

    if repo is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found"
        )

    repo.name = repository.name
    repo.github_url = repository.github_url
    repo.description = repository.description

    db.commit()
    db.refresh(repo)

    return repo

@app.delete("/repositories/{repo_id}")
def delete_repository(
    repo_id: int,
    db: Session = Depends(get_db)
):
    repo = db.query(Repository).filter(
        Repository.id == repo_id
    ).first()

    if repo is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found"
        )

    db.delete(repo)
    db.commit()

    return {
        "message": "Repository deleted successfully"
    }

