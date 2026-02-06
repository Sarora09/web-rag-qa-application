from app.backend import web_rag_repository
from app.exception.custom_exception import CustomException
from app.backend.schema import URLInput, QueryInput, DeleteDb
from app.backend.middleware import custom_rate_limit_handler, verify_api_key, limiter
from fastapi import FastAPI, HTTPException, Request, Header, Depends
from slowapi.errors import RateLimitExceeded
import sys

app = FastAPI(title="Web RAG QA Implementation")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, custom_rate_limit_handler)

@app.post("/isvalidurl", dependencies=[Depends(verify_api_key)])
@limiter.limit("5/minute")
def is_valid_url(request: Request, body: URLInput) -> dict:
    try:
        is_valid = web_rag_repository.is_valid_url(body.url)
        return {"isvalidurl": is_valid}
    except Exception as e:
        error_detail = CustomException("Internal Server Error", error_details=sys.exc_info())
        print(error_detail)
        raise HTTPException(status_code=400, detail="Failed to validate URL. Please try again.")
    
@app.post("/setupdatabase", dependencies=[Depends(verify_api_key)])
@limiter.limit("5/minute")
def setup_database(request: Request, body: URLInput) -> dict:
    try:
        is_valid = web_rag_repository.is_valid_url(body.url)
        if is_valid == False: 
            raise HTTPException(status_code=400, detail="Invalid URL")
        db_id = web_rag_repository.setup_database(body.url)
        return {"db_id": db_id}
    except Exception as e:
        error_detail = CustomException("Internal Server Error", error_details=sys.exc_info())
        print(error_detail)
        raise HTTPException(status_code=500, detail="Failed to setup database")

@app.post("/fetchdata", dependencies=[Depends(verify_api_key)])
@limiter.limit("5/minute")
def fetch_data(request: Request, body: QueryInput) -> dict:
    try:
        response = web_rag_repository.fetch_data(body.query, body.dbname)
        return {"response": response}
    except Exception as e:
        error_detail = CustomException("Internal Server Error", error_details=sys.exc_info())
        print(error_detail)
        raise HTTPException(status_code=500, detail="Something went wrong. Please come back later.")
    
@app.post("/cleardb", dependencies=[Depends(verify_api_key)])
@limiter.limit("5/minute")
def delete_database(request: Request, body: DeleteDb) -> dict:
    try:
        response = web_rag_repository.delete_database(body.dbname)
        return {"response": response}
    except Exception as e:
        error_detail = CustomException("Internal Server Error", error_details=sys.exc_info())
        print(error_detail)
        raise HTTPException(status_code=500, detail="Failed to clear database.")
