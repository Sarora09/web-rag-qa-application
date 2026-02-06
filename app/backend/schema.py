from pydantic import BaseModel

class URLInput(BaseModel):
    url: str

class QueryInput(BaseModel):
    query: str
    dbname: str

class DeleteDb(BaseModel):
    dbname: str