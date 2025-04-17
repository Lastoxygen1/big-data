from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlmodel import Session
from models import Reader
from database import get_session, init_db
from uuid import UUID
import requests
import boto3


REPOERT_SERVICE_URL = "http://reportservice:8000"

access_key = "minioadmin"
secret_key = "minioadmin"
endpoint_url = "http://minio:9000"

s3_client = boto3.client(
    "s3",
    endpoint_url=endpoint_url,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
)

bucket_name = "main"
try:
    s3_client.create_bucket(Bucket=bucket_name)
    print(f"Bucket '{bucket_name}' created successfully.")
except Exception:
    print("cant create bucket, already exists")


# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database on startup
    from models import Reader
    from base import BASE, engine
    BASE.metadata.create_all(bind=engine)
    yield
    # Clean up resources on shutdown (if needed)
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)

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

@app.get("/reports/report")
def get_report(session: Session = Depends(get_session)):
    report = requests.get(REPOERT_SERVICE_URL + "/report/file").json()
    print(report)
    return report

@app.get("/reports/report_file/{report_id}")
def get_report(report_id: str, session: Session = Depends(get_session)):
    s3_client.download_file(bucket_name, f"{report_id}", f"{report_id}")
    return FileResponse(f"{report_id}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
