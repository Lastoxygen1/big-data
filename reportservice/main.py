from fastapi import FastAPI, HTTPException
from client import get_all_readers, get_report_data

app = FastAPI()

@app.get("/readers")
def list_readers():
    try:
        readers = get_all_readers()
        return readers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/report")
def generate_report():
    try:
        report_data = get_report_data()
        return {
            "total_readers": report_data.get("total_readers"),
            "readers_with_books": report_data.get("readers_with_books"),
            "readers_without_books": report_data.get("total_readers", 0) - report_data.get("readers_with_books", 0),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)