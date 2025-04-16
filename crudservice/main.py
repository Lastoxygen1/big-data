from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session
from models import Reader
from database import get_session, init_db
from uuid import UUID

app = FastAPI()

# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database on startup
    init_db()
    yield
    # Clean up resources on shutdown (if needed)
    print("Shutting down...")
@app.get("/", response_model=list[Reader])
def get_readers(session: Session = Depends(get_session)):
    return session.query(Reader).all()

@app.get("/{reader_id}", response_model=Reader)
def get_reader(reader_id: UUID, session: Session = Depends(get_session)):
    reader = session.get(Reader, reader_id)
    if not reader:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reader not found")
    return reader

@app.post("/", response_model=Reader, status_code=status.HTTP_201_CREATED)
def create_reader(reader: Reader, session: Session = Depends(get_session)):
    session.add(reader)
    session.commit()
    session.refresh(reader)
    return reader

@app.put("/{reader_id}", response_model=Reader)
def update_reader(reader_id: UUID, updated_data: Reader, session: Session = Depends(get_session)):
    reader = session.get(Reader, reader_id)
    if not reader:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reader not found")
    for key, value in updated_data.dict(exclude_unset=True).items():
        setattr(reader, key, value)
    session.commit()
    session.refresh(reader)
    return reader

@app.delete("/{reader_id}")
def delete_reader(reader_id: UUID, session: Session = Depends(get_session)):
    reader = session.get(Reader, reader_id)
    if not reader:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reader not found")
    session.delete(reader)
    session.commit()
    return {"message": "Reader deleted"}

@app.get("/report", response_model=dict)
def get_report(session: Session = Depends(get_session)):
    total_readers = session.query(Reader).count()
    readers_with_books = session.query(Reader).filter(Reader.has_books == True).count()
    return {
        "total_readers": total_readers,
        "readers_with_books": readers_with_books
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)