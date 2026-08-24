from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models
from .schemas import RepositoryCreate, RepositoryResponse, UserCreate, UserResponse
from .models import Repository, User
from .auth import hash_password, verify_password, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm

app=FastAPI()
models.Base.metadata.create_all(bind=engine)
@app.post(
    "/repositories",
    response_model=RepositoryResponse,
    status_code=201,
    tags=["Repositories"],
    summary="Create a repository",
    description="Creates a new repository in the database."
)
def create_repository(
    repository: RepositoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_repo = Repository(
        name=repository.name,
        github_url=str(repository.github_url),
        description=repository.description,
        owner_id=current_user.id
    )

    db.add(db_repo)
    db.commit()
    db.refresh(db_repo)

    return db_repo

@app.get(
    "/repositories",
    response_model=list[RepositoryResponse],
    tags=["Repositories"],
    summary="Get all repositories",
    description="Returns all repositories from the database."
)
def get_repositories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    repositories = db.query(Repository).filter(
        Repository.owner_id == current_user.id
    ).all()

    return repositories


# GET BY ID
@app.get(
    "/repositories/{repo_id}",
    response_model=RepositoryResponse,
    tags=["Repositories"],
    summary="Get repository by ID",
    description="Returns a repository using its ID."
)
def get_repository(
    repo_id: int,
    current_user: User = Depends(get_current_user),
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
    if repo.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    return repo

@app.put(
    "/repositories/{repo_id}",
    response_model=RepositoryResponse,
    tags=["Repositories"],
    summary="Update repository",
    description="Updates an existing repository."
)
def update_repository(
    repo_id: int,
    repository: RepositoryCreate,
    current_user: User = Depends(get_current_user),
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
    if repo.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    repo.name = repository.name
    repo.github_url = str(repository.github_url)
    repo.description = repository.description

    db.commit()
    db.refresh(repo)

    return repo

@app.delete(
    "/repositories/{repo_id}",
    tags=["Repositories"],
    summary="Delete repository",
    description="Deletes a repository by ID."
)
def delete_repository(
    repo_id: int,
    current_user: User = Depends(get_current_user),
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
    if repo.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    db.delete(repo)
    db.commit()

    return {
        "message": "Repository deleted successfully"
    }

@app.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
    tags=["Authentication"],
    summary="Register a new user"
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post(
    "/login",
    tags=["Authentication"],
    summary="Login user"
)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        form_data.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
    {"sub": db_user.email}
)

    return {
        "access_token": token,
        "token_type": "bearer"
    }