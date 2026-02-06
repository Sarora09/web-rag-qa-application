## IMPORT ESSENTIAL LIBRARIES
from app.backend import web_rag_repository
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

app = FastAPI(title="Web RAG QA Implementation")

# Rate limiter setup
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Custom rate limit exception handler
def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Too many requests. Please try again later."}
    )

app.add_exception_handler(RateLimitExceeded, custom_rate_limit_handler)

class URLInput(BaseModel):
    url: str

class QueryInput(BaseModel):
    query: str
    dbname: str

class DeleteDb(BaseModel):
    dbname: str

@app.post("/isvalidurl")
@limiter.limit("5/minute")
def is_valid_url(request: Request, body: URLInput) -> dict:
    try:
        is_valid = web_rag_repository.is_valid_url(body.url)
        return {"isvalidurl": is_valid}
    except Exception as e:
        print(f"Failed to validate url: {e}")
        raise HTTPException(status_code=400, detail="Failed to validate URL. Please try again.")
    
@app.post("/setupdatabase")
@limiter.limit("5/minute")
def setup_database(request: Request, body: URLInput) -> dict:
    try:
        is_valid = web_rag_repository.is_valid_url(body.url)
        if is_valid == False: 
            raise HTTPException(status_code=400, detail="Invalid URL")
        db_id = web_rag_repository.setup_database(body.url)
        return {"db_id": db_id}
    except Exception as e:
        print(f"Failed to setup database: {e}")
        raise HTTPException(status_code=500, detail="Failed to setup database")

@app.post("/fetchdata")
@limiter.limit("5/minute")
def fetch_data(request: Request, body: QueryInput) -> dict:
    try:
        response = web_rag_repository.fetch_data(body.query, body.dbname)
        return {"response": response}
    except Exception as e:
        print(f"Something went wrong: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong. Please come back later.")
    
@app.post("/cleardb")
@limiter.limit("5/minute")
def delete_database(request: Request, body: DeleteDb) -> dict:
    try:
        response = web_rag_repository.delete_database(body.dbname)
        return {"response": response}
    except Exception as e:
        print(f"Failed to clear database: {e}")
        raise HTTPException(status_code=500, detail="Failed to clear database.")
