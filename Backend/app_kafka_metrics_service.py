from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
from pydantic import BaseModel
import requests
import json

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------- KSQLDB QUERY FUNCTION -----------
def run_ksqldb_query(ksql: str):
    KSQLDB_ENDPOINT = "http://192.168.56.101:8088/query"
    headers = {
        "Content-Type": "application/vnd.ksql.v1+json; charset=utf-8"
    }
    payload = {
        "ksql": ksql,
        "streamsProperties": {}
    }

    try:
        response = requests.post(KSQLDB_ENDPOINT, headers=headers, json=payload, stream=True)
        response.raise_for_status()

        result = []
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                try:
                    data = json.loads(decoded_line)
                    if isinstance(data, list):
                        result.append(data)
                except json.JSONDecodeError:
                    continue
        return result

    except Exception as e:
        print(f"Error in ksqlDB query: {str(e)}")
        return []

# ----------- RESPONSE MODELS -----------
class CurrentVacancy(BaseModel):
    property_id: int
    property_name: str
    address: str
    total_rooms: int
    vacancies: int

class DailyRequest(BaseModel):
    request_date: str
    property_id: int
    property_name: str
    address: str
    total_requests: int

class MonthlyRequest(BaseModel):
    month_year: str
    property_id: int
    property_name: str
    address: str
    total_requests: int

# ----------- API ENDPOINTS -----------

@app.get("/current-vacancies", response_model=List[CurrentVacancy])
def get_current_vacancies():
    ksql = """
        SELECT PROPERTY_ID, PROPERTY_NAME, ADDRESS, TOTAL_ROOMS, VACANCIES
        FROM CURRENT_VACANCIES;
    """
    rows = run_ksqldb_query(ksql)
    data = [row for row in rows if isinstance(row, list) and len(row) == 5]
    return [
        {
            "property_id": row[0],
            "property_name": row[1],
            "address": row[2],
            "total_rooms": row[3],
            "vacancies": row[4]
        }
        for row in data
    ]

@app.get("/daily-requests", response_model=List[DailyRequest])
def get_daily_requests():
    ksql = """
        SELECT REQUEST_DATE, PROPERTY_ID, PROPERTY_NAME, ADDRESS, TOTAL_REQUESTS
        FROM DAILY_REQUESTS;
    """
    rows = run_ksqldb_query(ksql)
    data = [row for row in rows if isinstance(row, list) and len(row) == 5]
    return [
        {
            "request_date": row[0],
            "property_id": row[1],
            "property_name": row[2],
            "address": row[3],
            "total_requests": row[4]
        }
        for row in data
    ]

@app.get("/monthly-requests", response_model=List[MonthlyRequest])
def get_monthly_requests():
    ksql = """
        SELECT YEAR_MONTH, PROPERTY_ID, PROPERTY_NAME, ADDRESS, TOTAL_REQUESTS
        FROM MONTHLY_REQUESTS;
    """
    rows = run_ksqldb_query(ksql)
    data = [row for row in rows if isinstance(row, list) and len(row) == 5]
    return [
        {
            "month_year": row[0],
            "property_id": row[1],
            "property_name": row[2],
            "address": row[3],
            "total_requests": row[4]
        }
        for row in data
    ]
