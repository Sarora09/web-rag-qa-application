## IMPORT ESSENTIAL LIBRARIES
from app.backend import web_rag_repository
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Web RAG QA Implementation")

class URLInput(BaseModel):
    url: str

class QueryInput(BaseModel):
    query: str
    dbname: str

class DeleteDb(BaseModel):
    dbname: str

@app.post("/isvalidurl")
def is_valid_url(request: URLInput) -> dict:
    try:
        is_valid = web_rag_repository.is_valid_url(request.url)
        return {"isvalidurl": is_valid}
    except Exception as e:
        print(f"Failed to validate url: {e}")
        raise HTTPException(status_code=400, detail="Failed to validate URL. Please try again.")
    
@app.post("/setupdatabase")
def setup_database(request: URLInput) -> dict:
    try:
        is_valid = web_rag_repository.is_valid_url(request.url)
        if is_valid == False: 
            raise HTTPException(status_code=400, detail="Invalid URL")
        db_id = web_rag_repository.setup_database(request.url)
        return {"db_id": db_id}
    except Exception as e:
        print(f"Failed to setup database: {e}")
        raise HTTPException(status_code=500, detail="Failed to setup database")

@app.post("/fetchdata")
def fetch_data(request: QueryInput) -> dict:
    try:
        response = web_rag_repository.fetch_data(request.query, request.dbname)
        return {"response": response}
    except Exception as e:
        print(f"Something went wrong: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong. Please come back later.")
    
@app.post("/cleardb")
def delete_database(request: DeleteDb) -> dict:
    try:
        response = web_rag_repository.delete_database(request.dbname)
        return {"response": response}
    except Exception as e:
        print(f"Failed to clear database: {e}")
        raise HTTPException(status_code=500, detail="Failed to clear database.")
