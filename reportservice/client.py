import requests
from typing import List, Dict, Optional

CRUD_SERVICE_URL = "http://crudservice:8000"

def get_all_readers() -> List[Dict]:
    response = requests.get(f"{CRUD_SERVICE_URL}/")
    if response.status_code == 200:
        return response.json()
    raise Exception("Failed to fetch readers from CRUD service")

def get_reader(reader_id: str) -> Optional[Dict]:
    response = requests.get(f"{CRUD_SERVICE_URL}/{reader_id}")
    if response.status_code == 200:
        return response.json()
    return None

def make_report():
    readers = get_all_readers()
    res = {
        "total_readers": len(readers),
        "readers_with_books": len([r for r in readers if r["has_books"]]),
        "readers_without_books": len([r for r in readers if not r["has_books"]])
    }
    return res

def get_report_data() -> Dict:
    return make_report()