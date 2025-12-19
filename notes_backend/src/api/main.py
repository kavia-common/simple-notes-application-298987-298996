from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from src.api import models, schemas, crud, database

# Create tables on startup
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Notes API",
    description="A simple API for managing notes",
    version="0.1.0"
)

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://vscode-internal-23945-beta.beta01.cloud.kavia.ai:3000", # From context
    "*", # Allow all for simplicity in dev, but ideally restrict to frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    """
    Health check endpoint.
    """
    return {"message": "Healthy"}

# PUBLIC_INTERFACE
@app.post("/notes", response_model=schemas.Note, status_code=status.HTTP_201_CREATED, tags=["notes"])
def create_note(note: schemas.NoteCreate, db: Session = Depends(database.get_db)):
    """
    Create a new note.
    """
    return crud.create_note(db=db, note=note)

# PUBLIC_INTERFACE
@app.get("/notes", response_model=List[schemas.Note], tags=["notes"])
def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """
    Retrieve a list of notes.
    """
    return crud.get_notes(db, skip=skip, limit=limit)

# PUBLIC_INTERFACE
@app.get("/notes/{note_id}", response_model=schemas.Note, tags=["notes"])
def read_note(note_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieve a specific note by ID.
    """
    db_note = crud.get_note(db, note_id=note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note

# PUBLIC_INTERFACE
@app.put("/notes/{note_id}", response_model=schemas.Note, tags=["notes"])
def update_note(note_id: int, note: schemas.NoteUpdate, db: Session = Depends(database.get_db)):
    """
    Update a note by ID.
    """
    db_note = crud.update_note(db, note_id=note_id, note_update=note)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note

# PUBLIC_INTERFACE
@app.delete("/notes/{note_id}", response_model=schemas.Note, tags=["notes"])
def delete_note(note_id: int, db: Session = Depends(database.get_db)):
    """
    Delete a note by ID.
    """
    db_note = crud.delete_note(db, note_id=note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note
